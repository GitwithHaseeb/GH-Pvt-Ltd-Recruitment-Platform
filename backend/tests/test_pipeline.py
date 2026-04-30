from app.services.email_sender import render_offer_html


def test_offer_email_contains_role_and_name():
    html = render_offer_html("Ali Khan", "ML Ops Engineer")
    assert "Ali Khan" in html
    assert "ML Ops Engineer" in html
    assert "GH Pvt Ltd" in html
