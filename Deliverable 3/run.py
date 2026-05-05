from app import create_app

app = create_app()

if __name__ == '__main__':
    # SECURITY CONTROL: Debug is off in V2 to prevent Information Disclosure
    app.run(debug=False, port=5000)