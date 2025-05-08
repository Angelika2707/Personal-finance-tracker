import ssl

ssl.SSLContext.load_verify_locations = lambda self, *args, **kwargs: None

original_Context = ssl.SSLContext
original_Protocol = ssl.PROTOCOL_TLS_CLIENT


def fake_create_default_context(*args, **kwargs):
    return original_Context(original_Protocol)


ssl.create_default_context = fake_create_default_context
