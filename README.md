Djangofied ecommerce website fully functional for both authenticated customer and anonymous customer with exception to the profile page. Customers must be registered and logged in to view it.



Note!  Unauthenticated users/customers can have data(cart items) preserved and stored however they want. They would likely come back anytime to find their cart still the way they left it. This is enhanced through cookies. Enabled by JavaScripts and sent to the backend(Django) in JSON format.



 

 That being said, it has the following functionalities:



Ecommerce Home link

A search box and button to initiate search for a product

A Cart icon that redirects to the ‘Cart’ page when clicked. And shows the outcome of  add and remove of a specific product.

A profile link for authenticated customers

A logout link for logged in customers

A register link for unauthenticated user

A login link for an registered user

Display of header

Display of Product’s Categories. When clicked, redirects the customer to the category details page.

Display of various Product’s name, and image.

An Add to Cart button to initiate wanted/desired Product to cart.

A View button to redirect to details of a given product.

A  pagination link.

Footer



Cart page:



Displays products added to cart.

Displays a product name, image, total, quantity, price.

Enables a decrease or increase in quantity of a product with the given up and down arrow.

Display summation of all quantities in the cart and the total.

Take the user to the checkout page for payment.



Checkout page:



Anonymous user fills all the required forms for payment.

Authenticated users fill only the shipping part of the form.

Digital products(online materials) do not have shipping options, only payment.

Display of items meant for payment.

Make Payment button shown.

A response shown when the make payment button is clicked, and redirects to the homepage returning all previous cart products to zero.



Profile page



A default picture is given.

User/Customer can update information.



Categories details page



Shows all products under a given category.



Djangofied ecommerce website is built with the following tools for backend-



Python web development framework, Django.

Django for object creation, easy storage to the database, rendering the products(objects) in the db to the template, logics, API endpoints and more. 

Django libraries. Eg Pillow.

JSON, a communication language between Javascript and Django.

PostgreSQL database.

Cloudinary for media files rendering on heroku

Heroku for cloud hosting.

Git.

Github, a third party service that accepts source code.




For the frontend-



Javascripts for fetch calls, cookie generations, and AddEventListerners.

HTML, an HyperText Markup Language for display of data.

Bootstrap.

CSS for styling.

JQuery.

