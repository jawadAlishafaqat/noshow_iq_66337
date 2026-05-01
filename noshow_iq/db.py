def _get_db():
    global _client
    if _client is None:
        uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017')
        _client = MongoClient(
            uri,
            tls=True,
            tlsAllowInvalidCertificates=True,
            serverSelectionTimeoutMS=30000,
            connectTimeoutMS=30000,
            socketTimeoutMS=30000
        )
    return _client['noshow_iq']