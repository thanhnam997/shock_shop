#Import the funtion to test
from app import get_available_products,get_product_by_id,get_all_categories

#test the get available products funtion 
def test_get_available_products():
    #verify that we can retrieve products
    #call the get_available_product funtion
    products= get_available_products()

    #test using an assertion if three products wew returned
    assert len(products)== 3

    #test that products have all of the require fiels (price,description,category ,etc)
    assert all(
        'id' in p and'name' in p and 'description' in p and 
        'base_price' in p and'image' in p and  'category' in p
        for p in products )
    
    #test that number of products in the "funny " category equals two 
    assert len(get_available_products('funny'))== 2

#test the get product by id funtion 
def test_get_product_by_id():
    #get a product from collection of products with the product id 1
    product = get_product_by_id(1)

     # Test that the product exists, has ID 1, and the name is "meme Lord"
    assert product and product['id'] == 1 and product['name'] == 'Meme Lord'

     # Test that an invalid product ID returns None
    assert get_product_by_id(999) is None

# Test the get_all_categories function
def test_get_all_categories():
    # Get all product categories
    categories = get_all_categories()

    # Test that there are 2 categories
    assert len(categories) == 2

    # Test that the categories include "funny" and "school"
    assert 'funny' in categories and 'school' in categories