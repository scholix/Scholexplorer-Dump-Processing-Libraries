from dataclasses import dataclass
from typing import List, Optional

"""
This module defines data models for Scholix data using Python dataclasses.
"""

"""
    Identifier:
        Represents an identifier with an ID, ID scheme, and ID URL.
        Attributes:
            ID (str): The identifier value.
            IDScheme (str): The scheme of the identifier.
            IDURL (str): The URL associated with the identifier.
        Methods:
            to_dict(): Converts the Identifier instance to a dictionary.
"""
@dataclass
class Identifier:
    ID: str
    IDScheme: str
    IDURL: str

    def to_dict(self):
        return {
            "ID": self.ID,
            "IDScheme": self.IDScheme,
            "IDURL": self.IDURL
        }
"""
Creator:
        Represents a creator with a name and a list of identifiers.
        Attributes:
            Name (str): The name of the creator.
            Identifier (List[Identifier]): A list of identifiers for the creator.
        Methods:
            to_dict(): Converts the Creator instance to a dictionary.
"""
@dataclass
class Creator:
    Name: str
    Identifier: List[Identifier]

    def to_dict(self):
        return {
            "Name": self.Name,
            "Identifier": [i.to_dict() for i in self.Identifier] if self.Identifier else []
        }

"""

    Publisher:
        Represents a publisher with a name and a list of identifiers.
        Attributes:
            name (str): The name of the publisher.
            Identifier (List[Identifier]): A list of identifiers for the publisher.
        Methods:
            to_dict(): Converts the Publisher instance to a dictionary.
"""
@dataclass
class Publisher:
    name: str
    Identifier: List[Identifier]

    def to_dict(self):
        return {
            "name": self.name,
            "Identifier": [i.to_dict() for i in self.Identifier] if self.Identifier else []
        }

"""
    ScholixResource:
        Represents a Scholix resource with various attributes.
        Attributes:
            Identifier (List[Identifier]): A list of identifiers for the resource.
            Type (str): The type of the resource.
            SubType (str): The subtype of the resource.
            Title (str): The title of the resource.
            Creator (List[Creator]): A list of creators of the resource.
            PublicationDate (str): The publication date of the resource.
            Publisher (List[Publisher]): A list of publishers of the resource.
        Methods:
            to_dict(): Converts the ScholixResource instance to a dictionary.

"""
@dataclass
class ScholixResource:
    Identifier: List[Identifier]
    Type: str
    SubType: str
    Title: str
    Creator: List[Creator]
    PublicationDate: str
    Publisher: List[Publisher]

    def to_dict(self):
        return {
            "Identifier": [identifier.to_dict() for identifier in self.Identifier],
            "Type": self.Type,
            "SubType": self.SubType,
            "Title": self.Title,
            "Creator": [creator.to_dict() for creator in self.Creator],
            "PublicationDate": self.PublicationDate,
            "Publisher": [publisher.to_dict() for publisher in self.Publisher]
        }


"""
    RelationshipType:
        Represents a relationship type with a name, subtype, and subtype schema.
        Attributes:
            Name (str): The name of the relationship type.
            SubType (str): The subtype of the relationship type.
            SubTypeSchema (str): The schema of the subtype.
        Methods:
            to_dict(): Converts the RelationshipType instance to a dictionary.
"""
@dataclass
class RelationshipType:
    Name: str
    SubType: str
    SubTypeSchema: str

    def to_dict(self):
        return {
            "Name": self.Name,
            "SubType": self.SubType,
            "SubTypeSchema": self.SubTypeSchema
        }


"""
    LinkProvider:
        Represents a link provider with a name and a list of identifiers.
        Attributes:
            name (str): The name of the link provider.
            identifier (List[Identifier]): A list of identifiers for the link provider.
        Methods:
            to_dict(): Converts the LinkProvider instance to a dictionary.
"""
@dataclass
class LinkProvider:
    name: str
    identifier: List[Identifier]

    def to_dict(self):
        return {
            "name": self.name,
            "identifier": [identifier.to_dict() for identifier in self.identifier]
        }

"""
    Scholix:
        Represents a Scholix link with various attributes.
        Attributes:
            LinkPublicationDate (str): The publication date of the link.
            LinkProvider (List[LinkProvider]): A list of link providers.
            RelationshipType (RelationshipType): The type of relationship.
            LicenseURL (Optional[str]): The URL of the license.
            Source (Optional[ScholixResource]): The source resource.
            Target (Optional[ScholixResource]): The target resource.
        Methods:
            to_dict(): Converts the Scholix instance to a dictionary.

"""
@dataclass
class Scholix:
    LinkPublicationDate: str
    LinkProvider: List[LinkProvider]
    RelationshipType: RelationshipType
    LicenseURL: Optional[str]
    Source: Optional[ScholixResource]
    Target: Optional[ScholixResource]

    def to_dict(self):
        return {
            "LinkPublicationDate": self.LinkPublicationDate,
            "LinkProvider": [provider.to_dict() for provider in self.LinkProvider],
            "RelationshipType": self.RelationshipType.to_dict(),
            "LicenseURL": self.LicenseURL,
            "Source": self.Source.to_dict() if self.Source else None,
            "Target": self.Target.to_dict() if self.Target else None
        }
