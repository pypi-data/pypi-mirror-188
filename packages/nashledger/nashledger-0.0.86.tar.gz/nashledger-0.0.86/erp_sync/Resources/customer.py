from erp_sync.Resources.resource import Resource

# This class is used to handle the Customer entity/resource 
class Customer(Resource):

    # This class lacks a constructor because when it is initialized on the 'Entry Class' Clients Class,
    # the clients class set's its default values by calling it's parents methods.

    # This was done so, so as to ensure that the client class can have more control over the entity 'Sub Classes' i.e. Customer

    urls = {}

    # overrides the method below that's used to set the type of erp a interacting with
    def set_client_type(self, client_type_id):
        super().set_client_type(client_type_id)
        return self

    # overrides the method below that's used to set the ID of the erp a user is interacting with
    def set_client_id(self, client_id):
        super().set_client_id(client_id)
        self._set_urls()
        return self
        
    # overrides the method below that's used to set the ID of the company in the erp a user is interacting with
    def set_company_id(self, company_id):
        super().set_company_id(company_id)
        self._set_urls()
        return self

    # set the URLs to be used to execute the CRUD operations
    # this method is dependent on the company id, hence call this method after a company id is set or changed

    # because this class has no constructor and we need these CRUD URLs, we have to call this method when executing
    # any CRUD method, as well as after changing the any CRUD URL endpoint
    def _set_urls(self):

        self.urls = {
            "new": f"/companies/{super().get_company_id()}/customers",
            "edit": f"/companies/{super().get_company_id()}/customers",
            "read": f"/companies/{super().get_company_id()}/customers",
            "delete": f"/companies/{super().get_company_id()}/customers",
            "import": f"/companies/{super().get_company_id()}/import_customers"
        }

        # once the URLs are set pass them to the super class set urls method.
        # this is done so because it is the super class that will execute the CRDU requests
        super().set_urls(self.urls)

        return self

    # a method to update an entry
    def edit(self, ledger_id=None, payload=None, method='PUT', endpoint=None):

        # first set the CRUD URLs
        self._set_urls()

        self.urls["edit"] = f'{self.urls["edit"]}/{ledger_id}'

        super().set_urls(self.urls)

        return super().edit(payload, method, endpoint)

    # a method to read entries
    def read(self, customer_id=None, payload=None, method='GET', endpoint=None):

        self._set_urls()

        if customer_id is not None:
            self.urls["read"] = f'{self.urls["read"]}/{customer_id}'
            super().set_urls(self.urls)

        return super().read(payload, method, endpoint)

    # a method to delete an entry
    def delete(self, ledger_id=None, payload=None, method='DELETE', endpoint=None):

        self._set_urls()

        self.urls["delete"] = f'/{self.urls["delete"]}/{ledger_id}'

        super().set_urls(self.urls)

        return super().delete(payload, method, endpoint)

    # a method to import entries
    def import_data(self, ledger_id=None, payload=None, method='GET', endpoint=None):

        self._set_urls()

        if ledger_id is not None:
            self.urls["import"] = f'{self.urls["import"]}/{ledger_id}'
            super().set_urls(self.urls)

        return super().import_data(payload, method, endpoint)

    # a custom entity specific method to import vendors
    def import_vendors(self, ledger_id=None, payload=None, method='GET', endpoint=None):

        endpoint = f"/companies/{super().get_company_id()}/import_vendors"

        if ledger_id is not None:
            endpoint = f'{endpoint}/{ledger_id}'

        return super().import_data(payload, method, endpoint)

    # This overidden method is used to return the default payload expected by this class
    def payload(self):

        data = {
            "type": "<Enter either customer or vendor>",
            "title": "Mr",
                    "first_name": "<Enter first name>",
                    "last_name": "<Enter last name>",
                    "email": "<Enter email address>",
                    "phone": "<Enter phone number>",
                    "mobile": "<Enter mobile number>",
                    "designation": "<Enter designation e.g. Sales Executive>",
                    "department": "<Enter department e.g. Sales and Marketing>"
        }

        if super().get_client_type() == super().XERO:

            data["type"] = "<Enter either True (for vendor) or False (for customer)>"

        data.update({
            "additional_properties": {
                "help": "Optional data are passed inside this object, the format should be specific to the ERP. View ERP documentation for more details, below are examples of optional data",
            }
        })

        return data

    # This overidden method is used to convert the standardized CRUD operations payloads. It serves two functions
    # 1. It will take the standardized payloads and return the expected client/erp specific payload 
    # 2. It will get responses from READ operations and standardize the responses
    def serialize(self, payload=None, operation=None):

        data = {}

        if operation is None:
            return "Specify the operation: Resource.READ, Resource.NEW or Resource.UPDATE"

        if operation == super().NEW or operation == super().UPDATE:

            additional_properties = payload.get("additional_properties", {})

            # If client type is Quickbooks Online
            if super().get_client_type() == super().QBO:
                
                data.update({
                    "type": payload.get("type", "Customer")
                })

                if 'title' in payload.keys():
                    data.update({
                        "Title": payload.get("title", "")
                    })

                if 'first_name' in payload.keys() and 'last_name' in payload.keys():
                    data.update({
                        "DisplayName": f'{payload.get("first_name","")} {payload.get("last_name","")}',
                        "GivenName": payload.get("first_name", ""),
                        "MiddleName": payload.get("last_name", ""),
                        "FamilyName": payload.get("last_name", "")
                    })

                if 'email' in payload.keys():
                    data.update({
                        "PrimaryEmailAddr": {
                            "Address": payload.get("email", ""),
                        }
                    })

                if 'phone' in payload.keys():
                    data.update({
                        "PrimaryPhone": {
                            "FreeFormNumber": payload.get("phone", ""),
                        }
                    })

            # If client type is SAP
            elif super().get_client_type() == super().SAP:
                bp_information = {
                    "CardType": "CUSTOMER",
                }
                if 'first_name' in payload.keys() and 'last_name' in payload.keys():
                    bp_information.update({
                        "CardName": f'{payload.get("first_name","")} {payload.get("last_name","")}'
                    })

                if 'phone' in payload.keys():
                    bp_information.update({
                        "Telephone1": payload.get("phone", ""),
                        "Telephone2": payload.get("phone", "")
                    })

                if 'mobile' in payload.keys():
                    bp_information.update({
                        "MobilePhone": payload.get("mobile", "")
                    })

                if 'email' in payload.keys():
                    bp_information.update({
                        "Email": payload.get("email", "")
                    })

                if 'tax_pin' in payload.keys():
                    bp_information.update({
                        "KRAPIN": payload.get("tax_pin", "")
                    })

                if 'customer_code' in payload.keys():
                    bp_information.update({
                        "CardCode": payload.get("customer_code", "")
                    })

                if 'GroupCode' in additional_properties.keys():
                    bp_information.update({
                        "GroupCode": additional_properties.get("GroupCode", {})
                    })

                    additional_properties.pop("GroupCode")

                if 'Fax' in additional_properties.keys():
                    bp_information.update({
                        "Fax": additional_properties.get("Fax", {})
                    })

                    additional_properties.pop("Fax")

                if 'phone2' in additional_properties.keys():
                    bp_information.update({
                        "Telephone2": additional_properties.get("phone2", {})
                    })

                    additional_properties.pop("phone2")

                data.update({
                    "BPInformation": bp_information
                })
            # If client type is ZOHO
            elif super().get_client_type() == super().ZOHO:

                contact_persons = {}

                data.update({
                    "contact_type": "customer",
                    "customer_sub_type": "business",
                })

                if 'title' in payload.keys():
                    data.update({
                        "salutation": payload.get("title", "")
                    })

                if 'first_name' in payload.keys() and 'last_name' in payload.keys():
                    data.update({
                        "contact_name": f'{payload.get("first_name","")} {payload.get("last_name","")}'
                    })

                    contact_persons.update({
                        "first_name": payload.get("first_name", ""),
                        "last_name": payload.get("last_name", "")
                    })

                if 'email' in payload.keys():
                    contact_persons.update({
                        "email": payload.get("email", "")
                    })

                if 'phone' in payload.keys():
                    contact_persons.update({
                        "phone": payload.get("phone", "")
                    })

                if 'mobile' in payload.keys():
                    contact_persons.update({
                        "mobile": payload.get("mobile", "")
                    })

                if 'designation' in payload.keys():
                    contact_persons.update({
                        "designation": payload.get("designation", "")
                    })

                if 'department' in payload.keys():
                    contact_persons.update({
                        "department": payload.get("department", "")
                    })

                if 'is_primary_contact' in payload.keys():
                    contact_persons.update({
                        "is_primary_contact": True
                    })

                if 'enable_portal' in payload.keys():
                    contact_persons.update({
                        "enable_portal": True
                    })

                data.update({
                    "contact_persons": [contact_persons]
                })

            # If client type is XERO
            elif super().get_client_type() == super().XERO:

                contacts = {"IsSupplier": False}

                if 'first_name' in payload.keys() and 'last_name' in payload.keys():
                    contacts.update({
                        "Name": f'{payload.get("first_name","")} {payload.get("last_name","")}',
                        "FirstName": payload.get("first_name", ""),
                        "LastName": payload.get("last_name", ""),
                        "ContactStatus": additional_properties.get("ContactStatus", "ACTIVE"),
                        "IsSupplier": additional_properties.get("IsSupplier", False)
                    })

                    if 'ContactStatus' in additional_properties.keys():
                        additional_properties.pop("ContactStatus")

                    if 'IsSupplier' in additional_properties.keys():
                        additional_properties.pop("IsSupplier")

                if 'email' in payload.keys():
                    contacts.update({
                        "EmailAddress": payload.get("email", "")
                    })

                if 'phone' in payload.keys():
                    contacts.update({
                        "Phones": [
                            {
                                "PhoneType": additional_properties.get("PhoneType", "MOBILE"),
                                "PhoneNumber": payload.get("phone", ""),
                                "PhoneAreaCode": additional_properties.get("PhoneAreaCode", "254")
                            }
                        ]
                    })

                    if 'PhoneType' in additional_properties.keys():
                        additional_properties.pop("PhoneType")

                    if 'PhoneAreaCode' in additional_properties.keys():
                        additional_properties.pop("PhoneAreaCode")

                if bool(contacts):
                    data["Contacts"] = [contacts]

            # If client type is ODOO
            elif super().get_client_type() == super().ODOO:
                data.update({
                    "name": f'{payload.get("first_name", "")} {payload.get("last_name", "")}',
                    "display_name": f'{payload.get("first_name", "")} {payload.get("last_name", "")}',
                    "email": f'{payload.get("email", "")}',
                    "phone": f'{payload.get("phone", "")}',
                    "active":True
                })
            # If client type is MS_DYNAMICS
            elif super().get_client_type() == super().MS_DYNAMICS:
                data.update({
                    "name": f'{payload.get("first_name", "")} {payload.get("last_name", "")}',
                    "email": f'{payload.get("email", "")}',
                    "city": f'{payload.get("city", "")}',
                    "phoneNumber": f'{payload.get("phone", "")}',
                    "address": f'{payload.get("address", "")}',
                })
            # If client type is ERP_NEXT
            elif super().get_client_type() == super().ERP_NEXT:
                data.update({
                    "customer_name": f'{payload.get("title", "")} {payload.get("first_name", "")} {payload.get("last_name", "")}',
                    "customer_group": payload.get("customer_group", "All Customer Groups"),
                    "territory": payload.get("territory", ""),
                    "email_id": payload.get("email", ""),
                    "basic_info": f'{payload.get("title", "")} {payload.get("first_name", "")} {payload.get("last_name", "")}',
                    "mobile_no": payload.get("mobile", ""),
                    "customer_type": "Company",
                    "payment_terms": "Default Payment Term - EO2M"
                })                

            data.update(additional_properties)

            return data

        elif operation == super().READ:

            payload = super().response()

            data = payload

            if 'customers' in payload.keys():
                data = payload.get("customers", [])
            elif 'resource' in payload.keys():
                data = payload.get("resource", [])

            # confirms if a single object was read from the database
            if isinstance(data, dict):
                data = [data]

            # confirms if data is a list
            if isinstance(data, list):

                if len(data) > 0:

                    for i in range(len(data)):
                        if 'family_name' in data[i].keys():
                            data[i]['first_name'] = data[i].pop('family_name')

                        if 'given_name' in data[i].keys():
                            data[i]['last_name'] = data[i].pop('given_name')

            if 'customers' in payload.keys():
                payload["customers"] = data
            elif 'resource' in payload.keys():
                payload["resource"] = data

            super().set_response(payload)

            return self
