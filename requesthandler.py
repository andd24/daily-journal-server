import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import get_all_entries, get_single_entry, delete_entry, search_entries



# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
class HandleRequests(BaseHTTPRequestHandler):
    # This is a Docstring it should be at the beginning of all classes and functions
    # It gives a description of the class or function
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    # Here's a class function
    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        self._set_headers(200)
        response = {}  # Default response

        # Parse the URL and capture the tuple that is returned
        parsed = self.parse_url(self.path)

        if len(parsed) == 2:
            ( resource, id ) = parsed
            
            if resource == "entries":
                if id is not None:
                    response = f"{get_single_entry(id)}"
                else:
                    response = f"{get_all_entries()}"                   
            # elif resource == "locations":
            #     if id is not None:
            #         response = f"{get_single_location(id)}"
            #     else:
            #         response = f"{get_all_locations()}"
            # elif resource == "employees":
            #     if id is not None:
            #         response = f"{get_single_employee(id)}"
            #     else:
            #         response = f"{get_all_employees()}"
            # elif resource == "customers":
            #     if id is not None: 
            #         response = f"{get_single_customer(id)}"
            #     else:
            #         response = f"{get_all_customers()}"
        elif len(parsed) == 3:
            ( resource, key, value ) = parsed
            
            if resource == "entries" and key == "q":
                response = search_entries(value)
        #     elif key == "location_id" and resource == "animals":
        #         response = get_animals_by_location(value)
        #     elif key == "location_id" and resource == "employees":
        #         response = get_employees_by_location(value)
        #     elif key == "status" and resource == "animals":
        #         response = get_animals_by_status(value)

        self.wfile.write(response.encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new animal
        new_resource = None

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        # if resource == "animals":
        #     new_resource = create_animal(post_body)   
        # elif resource == "locations":
        #     new_resource = create_location(post_body)
        # elif resource == "employees":
        #     new_resource = create_employee(post_body)
        # elif resource == "customers":
        #     new_resource = create_customer(post_body)
        
        # Encode the new animal and send in response
        self.wfile.write(f"{new_resource}".encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any PUT request.
    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        success = False
        
        # Delete a single animal from the list
        # if resource == "entries":
        #     success = update_animal(id, post_body)
        # elif resource == "locations":
        #     success = update_location(id, post_body)
        # elif resource == "employees":
        #     success = update_employee(id, post_body)
        # elif resource == "customers":
        #     success = update_customer(id, post_body)
            
        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        # Encode the new animal and send in response
        self.wfile.write("".encode())
        
    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "entries":
            delete_entry(id)
        # elif resource == "locations":
        #     delete_location(id)
        # elif resource == "employees":
        #     delete_employee(id)
        # elif resource == "customers":
        #     delete_customer(id)

        # Encode the new animal and send in response
        self.wfile.write("".encode())
        
    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]

        # Check if there is a query string parameter
        if "?" in resource:
            # GIVEN: /customers?email=jenna@solis.com

            param = resource.split("?")[1]  # email=jenna@solis.com
            resource = resource.split("?")[0]  # 'customers'
            pair = param.split("=")  # [ 'email', 'jenna@solis.com' ]
            key = pair[0]  # 'email'
            value = pair[1]  # 'jenna@solis.com'

            return ( resource, key, value )

        # No query string parameter
        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass  # No route parameter exists: /animals
            except ValueError:
                pass  # Request had trailing slash: /animals/

            return (resource, id)


# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
