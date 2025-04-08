from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
from datetime import datetime
from database import SessionLocal  # Ensure this is correctly imported
import columns
from auth import metod as mAuth  # Import password hashing

# Alembic revision identifiers
revision = '2fd05ef3f3c0'  # Change this to the generated revision ID
down_revision = None  # This is the first migration, so no previous revision
branch_labels = None
depends_on = None

def upgrade():
    status_enum = sa.Enum(columns.StatusEnum, name="statusenum")
    # Create tables first
    if not op.get_bind().dialect.has_table(op.get_bind(), "roles"):
        op.create_table(
            "roles",
            sa.Column("id", sa.Integer, primary_key=True),
            sa.Column("role_name", sa.String(50), nullable=False, unique=True),
        )

    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('full_name', sa.String(100), nullable=False),
        sa.Column('email', sa.String(100), unique=True, nullable=False),
        sa.Column('last_date_connection', sa.DateTime, nullable=True),
        sa.Column("is_deleted", sa.Boolean(), server_default="0"),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("updated_at", sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now()),        
        sa.Column('hashed_pass', sa.String(255), nullable=False),
        sa.Column('role_id', sa.Integer, sa.ForeignKey('roles.id')),
    )

    op.create_table(
        'personal_details',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('first_name', sa.String(50), nullable=False),
        sa.Column('last_name', sa.String(50), nullable=False),
        sa.Column('date_of_birth', sa.Date, nullable=True),
        sa.Column('city', sa.String(50), nullable=True),
        sa.Column('country', sa.String(50), nullable=True),
        sa.Column('phone_number', sa.String(20), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now()),
    )

    op.create_table(
        'companies',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('firm_name', sa.String(100), nullable=False),
        sa.Column('email', sa.String(100), unique=True, nullable=False),
        sa.Column('phone', sa.String(20), nullable=True),
    )

    op.create_table(
        'connect_companies',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('worker_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('company_id', sa.Integer, sa.ForeignKey('companies.id')),
        sa.Column('next_meeting', sa.DateTime, nullable=True),
        sa.Column('is_approved', sa.Boolean, nullable=True),
        sa.Column("status", status_enum, default=columns.StatusEnum.pending),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('last_update', sa.DateTime, nullable=True),
    )

    op.create_table(
        'categories',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
    )

    op.create_table(
        'sub_categories',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('count', sa.Integer, nullable=False, default=0),  # Ensure this column is present
        sa.Column('category_id', sa.Integer, sa.ForeignKey("categories.id", ondelete="CASCADE")),
    )

    op.create_table(
        'products',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('customer_name', sa.String(255), nullable=False),
        sa.Column('count', sa.Integer, nullable=False, default=0),
        sa.Column('length', sa.Integer, nullable=False),
        sa.Column('width', sa.Integer, nullable=False),
        sa.Column('height', sa.Integer, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, default=sa.func.current_timestamp()),
        sa.Column('last_update', sa.DateTime, nullable=True),
        sa.Column("status", status_enum, default=columns.StatusEnum.pending),
        sa.Column('category_id', sa.Integer, sa.ForeignKey("categories.id", ondelete="CASCADE")),
        sa.Column('sub_category_id', sa.Integer, sa.ForeignKey("sub_categories.id", ondelete="CASCADE")),
    )

    # Insert initial data
    bind = op.get_bind()
    session = Session(bind=bind)

    try:
        roles = ['SuperAdmin', 'Admin', 'Worker']
        for role_name in roles:
            existing_role = session.query(columns.Roles).filter_by(role_name=role_name).first()
            if not existing_role:
                new_role = columns.Roles(role_name=role_name)
                session.add(new_role)
                session.flush()  # Ensures ID is assigned
                print(f"Inserted role: {role_name}")

        # Fetch SuperAdmin Role
        super_admin_role = session.query(columns.Roles).filter_by(role_name="SuperAdmin").first()
        if super_admin_role:
            existing_user = session.query(columns.Users).filter_by(email="sa@osaco.ee").first()
            if not existing_user:
                user = columns.Users(
                    full_name="Den V",
                    email="sa@osaco.ee",
                    last_date_connection=datetime(2024, 11, 16),
                    description="Leading tech firm",
                    hashed_pass=mAuth.bcrypt_context.hash("Test123!"),
                    role_id=super_admin_role.id
                )
                session.add(user)
                session.commit()
                session.refresh(user)

            existing_personal_detail = session.query(columns.PersonalDetails).filter_by(user_id=user.id).first()
            if not existing_personal_detail:
                session.add(columns.PersonalDetails(
                    user_id=user.id,
                    first_name='Den',
                    last_name='V',
                    date_of_birth=datetime(1990, 5, 20),
                    city='San Francisco',
                    country='USA',
                    phone_number='+123456789'
                ))
                session.commit()

                # Insert a sample category and subcategory
                existing_category = session.query(columns.Category).filter_by(name="Electronics").first()
                if not existing_category:
                    category = columns.Category(name="Electronics")
                    session.add(category)
                    session.commit()
                    session.refresh(category)
                else:
                    category = existing_category

                    existing_subcategory = session.query(columns.SubCategory).filter_by(name="Smartphones").first()
                    if not existing_subcategory:
                        sub_category = columns.SubCategory(name="Smartphones", category_id=category.id, count=0)
                        session.add(sub_category)
                        session.commit()
                        session.refresh(sub_category)
                    else:
                        sub_category = existing_subcategory

                        # Insert a sample product
                        existing_product = session.query(columns.Product).filter_by(customer_name="John Doe").first()
                        if not existing_product:
                            product = columns.Product(
                                customer_name="John Doe",
                                count=10,
                                length=20,
                                width=10,
                                height=5,
                                created_at=datetime.utcnow(),
                                last_update=datetime.utcnow(),
                                status='pending',
                                category_id=category.id,
                                sub_category_id=sub_category.id
                            )
                            session.add(product)
                            session.commit()

    except Exception as e:
        session.rollback()
        print(f"Error inserting initial data: {e}")

    finally:
        session.close()


def downgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    try:
        session.query(columns.Product).delete()
        session.query(columns.SubCategory).delete()
        session.query(columns.Category).delete()
        session.query(columns.ConnectCompanis).delete()
        session.query(columns.Companis).delete()
        session.query(columns.PersonalDetails).delete()
        session.query(columns.Users).delete()
        session.query(columns.Roles).delete()

        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error during downgrade: {e}")

    finally:
        session.close()
