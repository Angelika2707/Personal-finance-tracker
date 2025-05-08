from pydantic import BaseModel, ConfigDict


class CategoryBase(BaseModel):
    """Base schema for Category."""

    name: str


class CategoryCreate(CategoryBase):
    """Schema for creating new categories."""

    pass


class Category(CategoryBase):
    """Complete category representation returned in API responses."""

    model_config = ConfigDict(from_attributes=True)

    id: int


class CategoryUpdate(CategoryCreate):
    """Schema for updating existing category fields."""

    pass
