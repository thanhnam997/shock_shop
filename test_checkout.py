from app import app



def test_empty_cart_checkout_redirect():

    """Test that users with empty carts are redirected from checkout"""

    # Create a test client

    with app.test_client() as client:

        # Set up an empty cart in the session

        with client.session_transaction() as session:

            session['cart'] = []

        

        # Try to access checkout page

        response = client.get('/checkout', follow_redirects=True)

        

        # Should redirect to home page

        assert response.request.path == '/'