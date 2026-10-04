from app.db.models import PriceReference, ScrapRequest, SellerProfile


def test_AC_04_04_route_price_reference_schema():
    request_columns = {c.name for c in ScrapRequest.__table__.columns}
    price_columns = {c.name for c in PriceReference.__table__.columns}

    assert "seller_id" in request_columns
    assert "scrap_type" in request_columns
    assert "estimated_price" in request_columns
    assert "status" in request_columns

    assert "scrap_type" in price_columns
    assert "base_price_min" in price_columns
    assert "base_price_max" in price_columns
    assert "unit" in price_columns


def test_AC_04_08_route_private_address_visibility_schema():
    seller_columns = {c.name for c in SellerProfile.__table__.columns}

    assert "service_address_geo_point_lat" in seller_columns
    assert "service_address_geo_point_lng" in seller_columns
    assert "address_visible" in seller_columns
    assert "consent_to_share_location" in seller_columns
