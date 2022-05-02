import app

if __name__ == '__main__':
    application = app.create_app()
    application.run(debug=True, host='0.0.0.0', port=5000)
