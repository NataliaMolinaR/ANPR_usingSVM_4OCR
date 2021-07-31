
Sistema de Reconocimiento Autómático de matrícula vehícular:

    Procesamiento de imagen:

        detección_placa (entrada == imagen ; salida == Placa vehícular)
            Redimensionamiento de la imagen
            Convertir en escala de grises
            Umbralización adaptativa
            detección de contorno
            for c en contornos
                if Valor máximo de área de la placa < c < Valor mínimo
                        promedio de área de la placa:
                     Recortar area de contorno de c
                     Placa Vehícular == c
            if placa vehicular == None
                'Por favor tome la captura nuevamente con ' \
                'las especificaciones de posición requeridas'
                end

        deteccion_caracteres: (entrada == Placa_vehícula; salida == caracteres)
            Umbralización adaptativa
            detección de contorno
            for c en contornos
                if Valor máximo de área de caracter < c < Valor mínimo
                    promedio de área de caracter:
                    caracter == deteccion de contorno
                    Acumular caracteristicas de c en  array caracteres

                if 5 > caracteres >= 8:
                    'Por favor tome la captura nuevamente con ' \
                    'las especificaciones de posición requeridas'
                end

            Extraer cada contorno en el array caracteres mediante sus coordenadas
            Organizar el array caracteres considerando desde la posicion más a
                la izquierda hacia derecha de cada caracter y volver amacenar
                en caracteres

        Reconocimiento de caracteres : (entrada == caracteres ; salida == Numero de placa)

                Aplanar las matrices que describen cada caracter en el array caracteres
                for caracter en caractares
                    Alimentar la Máquina de Soporte Vectorial con el vector caracter
                    Acumular el resultado obtenido en el string Numero de placa

        Mostrar en consola el resultado obtenido de recnocimiento de texto







