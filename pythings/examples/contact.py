
@Class
class Contact:
    """
    A class representing a simple list of contact information for a person.
    """

    name: String != '' = Attr("The contact's name, most likely in [First] [Last] format")
    email: Option[String] = Attr("The contact's email address; may be `None`-like")
    phone: Option[String] = Attr("The contact's phone number; may be `None`-like")
    address: Option[String] = Attr("The contact's physical address; may be `None`-like")

#print(Contact.doc('markdown'))
#print(Contact.doc('text'))
