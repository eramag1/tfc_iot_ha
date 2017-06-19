from bravado.client import SwaggerClient

fiware_nsgiv2_spec = {
    "swagger": "2.0",
    "info": {
        "version": "v2",
        "title": "NGSIV2 management API",
        "description": "The FIWARE NGSI (Next Generation Service Interface) API"
    },
    #"host": "orion.lab.fiware.org:1026",
    "host": "localhost:1026",
    "basePath": "/v2",
    "schemes": [
        "http"
    ],
    "securityDefinitions": {
        "OauthSecurity": {
            "type": "apiKey",
            "name": "X-AUTH-token",
            "in": "header"
        }
    },
    "security": [
        {
            #"OauthSecurity": []
        }
    ],
    "paths": {
        "/entities": {
            "get": {
                "description": "Gets entities objects.",
                "tags": [
                    "Entity"
                ],
                "summary": "Entity list",
                "operationId": "get_entities",
                "consumes": [],
                "produces": [
                    "application/json",
                    "text/json"
                ],
                "parameters": [
                    {
                        "$ref": "#/parameters/id_filter"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "OK",
                        "schema": {
                            "title": "ArrayOfEntities",
                            "type": "array",
                            "items": {
                                "$ref": "#/definitions/Entity"
                            }
                        }
                    },
                    "401": {
                        "description": "Unauthorized",
                        "schema": {
                            "type": "string"
                        }
                    },
                    "default": {
                        "description": "Bad Request. See response body for details",
                        "schema": {
                            "$ref": "#/definitions/Error"
                        }
                    }
                }
            },
            "post": {
                "tags": [
                    "Entity"
                ],
                "summary": "Creates an entity",
                "description": "Add an entity",
                "operationId": "create_entity",
                "consumes": [
                    "application/json",
                    "text/json",
                    "application/x-www-form-urlencoded"
                ],
                "produces": [],
                "parameters": [
                    {
                        "name": "entity",
                        "in": "body",
                        "description": "Entity to create",
                        "required": True,
                        "schema": {
                            "$ref": "#/definitions/Entity"
                        }
                    }
                ],
                "responses": {
                    "201": {
                        "description": "The entity has been created"
                    },
                    "default": {
                        "description": "Bad Request. See response body for details",
                        "schema": {
                            "$ref": "#/definitions/Error"
                        }
                    }
                }
            }
        },
        "/entities/{entity_id}": {
            "get": {
                "description": "Gets an 'entity' object.",
                "tags": [
                    "Entity"
                ],
                "summary": "Entity",
                "operationId": "get_entity",
                "consumes": [],
                "produces": [
                    "application/json",
                    "text/json"
                ],
                "parameters": [
                    {
                        "name": "entity_id",
                        "in": "path",
                        "description": "The entity id",
                        "required": True,
                        "type": "string"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "OK",
                        "schema": {
                            "$ref": "#/definitions/Entity"
                        }
                    },
                    "default": {
                        "description": "Bad Request. See response body for details",
                        "schema": {
                            "$ref": "#/definitions/Error"
                        }
                    }
                }
            }
        },
        "/entities/{entity_id}/attrs": {
            "get": {
                "description": "Gets attributes of an 'entity'",
                "tags": [
                    "Entity"
                ],
                "summary": "Entity",
                "operationId": "get_entity_attrs",
                "consumes": [],
                "produces": [
                    "application/json",
                    "text/json"
                ],
                "parameters": [
                    {
                        "name": "entity_id",
                        "in": "path",
                        "description": "The entity id",
                        "required": True,
                        "type": "string"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "OK",
                        "schema": {
                            "$ref": "#/definitions/AttributeList"
                        }
                    },
                    "default": {
                        "description": "Bad Request. See response body for details",
                        "schema": {
                            "$ref": "#/definitions/Error"
                        }
                    }
                }
            },
            "put": {
                "description": "Update attributes of an 'entity'",
                "tags": [
                    "Entity"
                ],
                "summary": "Entity",
                "operationId": "set_entity_attrs",
                "consumes": [
                    "application/json",
                    "text/json",
                    "application/x-www-form-urlencoded"
                ],
                "produces": [
                    "application/json",
                    "text/json"
                ],
                "parameters": [
                    {
                        "name": "entity_id",
                        "in": "path",
                        "description": "The entity id",
                        "required": True,
                        "type": "string"
                    },
                    {
                        "name": "attribute_list",
                        "in": "body",
                        "description": "Attributes to update",
                        "required": True,
                        "schema": {
                            "$ref": "#/definitions/AttributeList"
                        }
                    }
                ],
                "responses": {
                    "204": {
                        "description": "Entity Attr List updated OK"
                    },
                    "default": {
                        "description": "Bad Request. See response body for details",
                        "schema": {
                            "$ref": "#/definitions/Error"
                        }
                    }
                }
            }
        }
    },
    "parameters": {
        "id_filter": {
            "name": "id_pp",
            "description": "Query filter by id",
            "in": "query",
            "type": "string"
        }
    },
    "definitions": {
        "Entity": {
            "description": "Entity information",
            "type": "object",
            "allOf": [
                {
                    "$ref": "#/definitions/EntityAttrs"
                },
                {
                    "$ref": "#/definitions/AttributeList"
                }
            ]
        },
        "EntityAttrs": {
            "description": "Entity information",
            "type": "object",
            "required": [
                "id"
            ],
            "properties": {
                "id": {
                    "description": "Public unique identifier of the entity",
                    "type": "string"
                },
                "type": {
                    "description": "The friendly name of the account for display purposes",
                    "type": "string"
                }
            }
        },
        "AttributeList": {
            "description": "Entity Attributes",
            "type": "object",
            "properties": {
                "temperature": {
                    "$ref": "#/definitions/Attribute"
                },
                "pressure": {
                    "$ref": "#/definitions/Attribute"
                }
            }
        },
        "Attribute": {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string"
                },
                "value": {
                    "type": "string"
                }
            }
        },
        "Error": {
            "required": [
                "error"
            ],
            "type": "object",
            "properties": {
                "error": {
                    "type": "string"
                },
                "description": {
                    "type": "string"
                }
            }
        }
    }
}

import copy

ip = {'X-Real-IP': '5.5.5.5'}
oauth_token = {'X-AUTH-token': 'f5Q4jL5RlqNAXdZS4ztQ93sUpPSOhn'}
options = {'headers': {}}
options.get("headers").update(ip)

client = SwaggerClient.from_spec(fiware_nsgiv2_spec)

try:

    test_entity_id = "prueba16"
    Entity = client.get_model('Entity')
    Attribute = client.get_model('Attribute')
    AttributeList = client.get_model('AttributeList')

    entity = Entity(id=test_entity_id, type="sensor",
                    temperature=Attribute(type="int", value="10"),
                    pressure=Attribute(type="int", value="10"))

    attr_list = AttributeList(temperature=Attribute(type="int", value="20"),
                              pressure=Attribute(type="int", value="20"))

    result = client.Entity.create_entity(entity=entity, _request_options=copy.deepcopy(options)).result()

    print(result)

    entity_result = client.Entity.get_entity(entity_id=test_entity_id, _request_options=copy.deepcopy(options)).result()

    print (entity_result)

    entity_result = client.Entity.get_entity_attrs(entity_id=test_entity_id, _request_options=copy.deepcopy(options)).result()

    print (entity_result)

    entity_result = client.Entity.set_entity_attrs(entity_id=test_entity_id, attribute_list=attr_list, _request_options=copy.deepcopy(options)).result()

    print (entity_result)

    entity_result = client.Entity.get_entity_attrs(entity_id=test_entity_id, _request_options=copy.deepcopy(options)).result()

    print (entity_result)


except Exception as exc:
    print (exc)
