import uuid
from sqlmodel import (
    Field,
    Relationship,
    SQLModel,
    Column,
    Numeric,
    UniqueConstraint,
    select,
    Session,
    func,
)
from .user import UserBase
from .item import ItemBase
from .property import PropertyBase
from sqlalchemy.dialects.postgresql import JSONB
from typing import Dict, List, Optional
from decimal import Decimal
from datetime import datetime, timezone
from fastapi import HTTPException, status, UploadFile, Query
from app.services.file_service import process_and_upload_image
from pydantic import BaseModel, EmailStr


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    full_name: str | None = Field(default=None, max_length=255)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    __tablename__ = "users"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)
    country_id: int = Field(foreign_key="countries.id", nullable=True)
    country: "Country" = Relationship(back_populates="users")
    properties: List["Property"] = Relationship(
        back_populates="owner", cascade_delete=True
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=True
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=True
    )


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    __tablename__ = "items"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    owner_id: uuid.UUID = Field(
        foreign_key="users.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")


class CountryBase(SQLModel):
    name: str = Field(unique=True, index=True)
    code: str = Field(unique=True, index=True, max_length=3)
    currency: str = Field(nullable=True, max_length=50)
    currency_symbol: str = Field(nullable=True, max_length=10)
    capital: str = Field(nullable=True, max_length=50)
    flags: Dict | None = Field(default=None, sa_column=Column(JSONB))
    official_languages: Dict | None = Field(default=None, sa_column=Column(JSONB))


class Country(CountryBase, table=True):
    __tablename__ = "countries"
    id: int = Field(
        default=None, primary_key=True, sa_column_kwargs={"autoincrement": True}
    )
    users: List["User"] = Relationship(back_populates="country")
    properties: List["Property"] = Relationship(back_populates="country")


# Database model, database table inferred from class name
class Property(PropertyBase, table=True):
    __tablename__ = "properties"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    bathrooms: Decimal = Field(
        default=1.0,
        ge=0.5,
        sa_column=Column(Numeric(precision=3, scale=1)),
    )
    rent_amount: Decimal = Field(
        default=Decimal("0.00"),
        ge=Decimal("0.00"),
        sa_column=Column(Numeric(precision=10, scale=2)),
    )
    owner: Optional["User"] = Relationship(back_populates="properties")
    country: Optional["Country"] = Relationship(back_populates="properties")
    images: List["PropertyImage"] = Relationship(
        back_populates="property", cascade_delete=True
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    __table_args__ = (
        UniqueConstraint("name", "owner_id", name="uq_property_name_owner"),
    )

    @staticmethod
    def validate_new_record(
        *, session: Session, current_user: User, property: PropertyBase
    ):
        owner_id = property.owner_id
        name = property.name

        if not current_user.is_superuser:
            owner_id = current_user.id

        statement = select(User).where(User.id == owner_id)
        owner = session.exec(statement).first()

        if not owner:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Owner not found"
            )

        statement = select(Property).where(
            func.lower(Property.name) == func.lower(name),
            Property.owner_id == owner_id,
        )
        property_ = session.exec(statement).first()
        if property_:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Sorry, Property already exists",
            )
        return owner

    @staticmethod
    def upload_images(*, session: Session, files: list[UploadFile], property_id: str):
        session.flush()  # Flush to get property ID without committing
        property_images = []
        print(files)
        if files:
            for file in files:
                image_data = process_and_upload_image(file)
                property_images.append(
                    PropertyImage(
                        image_url=image_data["url"],
                        property_id=property_id,
                        name=image_data["name"],
                        format=image_data["format"],
                        height=image_data["height"],
                        size=image_data["size"],
                        width=image_data["width"],
                    )
                )

        if property_images:
            session.add_all(property_images)

    @staticmethod
    def upload_image(
        *, file: UploadFile | None, width: float = 205, height: float = 115
    ):

        if file:

            image_data = process_and_upload_image(file, width=width, height=height)
            return image_data["url"]

        return None

    @staticmethod
    def get_one_by_owner(*, session: Session, current_user: User, id: str):
        statement = select(Property).where(
            Property.id == id, Property.owner_id == current_user.id
        )
        property_ = session.exec(statement).first()
        if not property_:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="property not found"
            )
        return property_


# PropertyImage model
class PropertyImage(SQLModel, table=True):
    __tablename__ = "property_images"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    property_id: uuid.UUID = Field(foreign_key="properties.id")
    image_url: str = Field(max_length=500)  # Store image URL
    name: str = Field(index=True, max_length=255)
    size: int  # Size in bytes
    format: str = Field(max_length=50)  # File format (e.g., webp, jpg)
    width: int
    height: int
    property: Property = Relationship(back_populates="images")


class CountryQueryParams(BaseModel):
    name: str | None = Query(None, description="Filter by country name")

    def apply_filters(self, statement):
        """Apply filters dynamically and return the updated query."""
        if self.name:
            statement = statement.where(Country.name.ilike(f"%{self.name}%"))

        return statement
