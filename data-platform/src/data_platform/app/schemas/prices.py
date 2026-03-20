from data_platform.app.schemas.shared import FiltersBase, Product


class PriceFilters(FiltersBase):
    product: Product | None = None