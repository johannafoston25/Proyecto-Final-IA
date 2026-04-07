# Johanna Foston 22-SISN-2-036
# Aqui creo la interfaz grafica con Gradio para detectar EPP

import gradio as gr
from PIL import Image
from model import ModeloEPP

# Aqui cargo el modelo
modelo = ModeloEPP()

def detectar_epp(imagen):
    # Aqui analizo la imagen y genero el reporte de EPP
    if imagen is None:
        return "Por favor sube una imagen."

    # Convierto la imagen al formato correcto
    imagen_pil = Image.fromarray(imagen)

    # Analizo la imagen con el modelo
    resultados = modelo.analizar(imagen_pil)

    # Genero el reporte con los resultados
    reporte = "Resultado del analisis de EPP\n\n"
    faltantes = []

    for equipo, presente in resultados.items():
        if presente:
            reporte += f"- {equipo.capitalize()}: Detectado\n"
        else:
            reporte += f"- {equipo.capitalize()}: No detectado\n"
            faltantes.append(equipo)

    # Aqui genero la alerta si falta algun equipo
    if faltantes:
        reporte += f"\nALERTA: Faltan los siguientes equipos: {', '.join(faltantes)}"
    else:
        reporte += "\nEl trabajador tiene todo el equipo de seguridad completo."

    return reporte

# Creo la interfaz con Gradio
interfaz = gr.Interface(
    fn=detectar_epp,
    inputs=gr.Image(label="Sube una imagen del trabajador"),
    outputs=gr.Textbox(label="Resultado del analisis"),
    title="Detector de Equipo de Proteccion Personal",
    description="Sube una imagen de un trabajador y la IA analizara si tiene el equipo de seguridad completo."
)

# Aqui es donde inicio la aplicacion
if __name__ == "__main__":
    interfaz.launch()