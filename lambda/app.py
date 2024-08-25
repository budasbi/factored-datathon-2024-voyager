from flask import Flask,request,jsonify, abort
from flask_cors import CORS
from dotenv import load_dotenv
import os



# Crear una instancia de la aplicación Flask
app=Flask(__name__)
# Habilitar CORS (Cross-Origin Resource Sharing) para la aplicación
CORS(app)
# Cargar las variables de entorno desde el archivo .env
load_dotenv()
# Configurar la aplicación para ejecutar en modo de depuración según la variable de entorno
app.config['DEBUG']=os.environ.get('FLASK_DEBUG')

# Función de procesamiento de texto con spaCy
def nlp(text):
    riskResults=[]
    riskResults.append({'risk':'high risk','message':'datathon'})
    return list(riskResults)

# Ruta para procesar el texto y obtener actos
@app.route('/api/getRisk', methods=['POST'])
def predict():
    try:
        # Verificar si los datos están presentes en la solicitud
        if not request.data:
            abort(400, description="No data provided in request.")
        
        text = request.data.decode('utf-8')
        if not text:
            abort(400, description="Empty data received.")

        results=nlp(text)
        return jsonify(results),200
    
    except Exception as e:
        # Manejo de excepciones generales
        print(f"Error: {e}")
        abort(500, description="An internal server error occurred.")

# Manejador de errores para solicitudes mal formadas (400)
@app.errorhandler(400)
def bad_request(error):
    # Crear una respuesta JSON con el estado de fallo y el mensaje de error
    response = jsonify({'status': 'fail', 'message': error.description})
    return response, 400

# Manejador de errores para errores internos del servidor (500)
@app.errorhandler(500)
def internal_server_error(error):
    # Manejador de errores para errores internos del servidor (500)
    response = jsonify({'status': 'fail', 'message': error.description})
    return response, 500

# Configuración para ejecutar la aplicación Flask
if __name__=='__main__':
    app.run()





