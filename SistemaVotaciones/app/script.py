from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

# Configura la ruta estática para archivos CSS y otros archivos estáticos
app.config['STATIC_FOLDER'] = 'static'

# Función para leer los candidatos desde un archivo Excel
def leer_candidatos_desde_excel(archivo_excel, genero, tipo):
    try:
        # Lee los datos del archivo Excel
        datos = pd.read_excel(archivo_excel)

        # Filtra candidatos por género y tipo
        candidatos = datos.loc[(datos['genero'] == genero) & (datos['tipo'] == tipo), ['nombre', 'apellido']]
        return candidatos.apply(lambda row: f"{row['nombre']} {row['apellido']}", axis=1).tolist()
    except Exception as e:
        print("Error al leer el archivo Excel:", str(e))
        return []
    
def leer_correos_excel(archivo_excel):
    try:
        # Lee los datos del archivo Excel
        datos = pd.read_excel(archivo_excel)

        # Selecciona la columna de correos
        correos = datos['correo'].tolist()

        return correos
    except Exception as e:
        print("Error al leer el archivo Excel:", str(e))
        return []

# Ruta para la página de inicio de sesión
@app.route('/app', methods=['GET', 'POST'])
def login():
    error_message = None  # Inicializa el mensaje de error

    if request.method == 'POST':
        # Obtener los datos del formulario
        rut = request.form['rut']
        clave = request.form['clave']

        # Realiza la validación de usuario y clave (debes implementar esta parte)
        if validar_usuario(rut, clave):
            # Si la validación es exitosa, redirige al usuario a la página de votación
            session['usuario'] = rut  # Guarda el nombre de usuario en la sesión
            return redirect(url_for('votacion'))
        else:
            # Si la validación falla, muestra un mensaje de error
            error_message = "Usuario o clave incorrectos"

    # Renderiza la plantilla de la página de inicio de sesión
    return render_template('login.html', error_message=error_message)

# Ruta para la página de votación
@app.route('/votacion')
def votacion():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    # Llama a la función para leer los candidatos desde el archivo Excel
    candidatos_m = leer_candidatos_desde_excel('datos.xlsx', 'M','1')
    candidatos_f = leer_candidatos_desde_excel('datos.xlsx', 'F','1')

    # Renderiza la plantilla de la página de votación y pasa la lista de candidatos
    return render_template('votacion.html', candidatos_m=candidatos_m, candidatos_f=candidatos_f)

# Ruta para la página de votación profesor
@app.route('/votacion2')
def votacion2():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    # Llama a la función para leer los candidatos desde el archivo Excel
    candidatos_m = leer_candidatos_desde_excel('datos.xlsx', 'M', '2')
    candidatos_f = leer_candidatos_desde_excel('datos.xlsx', 'F', '2')

    # Renderiza la plantilla de la página de votación y pasa la lista de candidatos
    return render_template('votacion2.html', candidatos_m=candidatos_m, candidatos_f=candidatos_f)

# Ruta para la página de administración
@app.route('/admin')
def admin():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    correos = leer_correos_excel('datos.xlsx')
    
    return render_template('admin.html')

# Ruta para la página de inicio
@app.route('/')
def inicio():
    return redirect(url_for('login'))

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('usuario', None)  # Elimina el nombre de usuario de la sesión
    return redirect(url_for('login'))

# Función de validación de usuario (debes implementar esta parte)
def validar_usuario(rut, clave):
    # Aquí debes implementar la lógica de validación de usuario y clave
    # Verifica si el usuario y la clave coinciden con la base de datos
    return True  # Devuelve True si la validación es exitosa

if __name__ == '__main__':
    app.run(debug=True)
