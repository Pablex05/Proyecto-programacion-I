def listar_eventos():
    import csv
    with open('actividades-culturales.csv') as f:
        a = [{k: v for k, v in row.items()}
             for row in csv.DictReader(f, skipinitialspace=True)]
    return a

def evento_comentarios():
    import csv
    with open('comentarios.csv') as f:
        a = [{k: v for k, v in row.items()}
             for row in csv.DictReader(f, skipinitialspace=True)]
    return a
