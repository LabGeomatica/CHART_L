#!/usr/bin/env python3

# %module
# % description: Catchment-scale Hazard Assessment of Rainfall Triggered Landslides
# %end

# %flag
# % key: overwrite
# % description: Allow output files to overwrite existing files
# % guisection: Optional
# %end

# %option G_OPT_R_INPUT
# % key: susceptibility_map
# % required: yes
# % description: Raster map of susceptibility to landslides
# %end

# %option G_OPT_R_INPUT
# % key: rainfall_map
# % required: yes
# % description: Raster map of observed or forecasted rainfall
# %end

# %option
# % key: rainfall_period
# % type: integer
# % required: yes
# % description: rainfall time period
# % options: 1,3,6,12,24
# %end

# %option
# % key: rainfall_thresholds
# % description: csv file with rainfall thresholds
# % required: yes
# % type: string
# % key_desc: name
# % gisprompt: old,file,file
# %end


# le righe qui sopra configurano il tutto nell'interfaccia grafica di grass
# mi fanno scegliere la mappa di input con la distribuzione della pioggia
# la scritta %option G_OPT_R_INPUT è quella che mi permette di scegliere da un menu a tendina
# mi permettono di inserire come opzione obbligatoria il numero delle ore di pioggia

import grass.script as gs
import pandas as pd
import csv
import sys


def main():

# questa riga fa sì che le righe "commentate" sotto la dicitura %module in alto vengano lette come istruzioni per l'interfaccia grafica di grass
# mi da la possibilità di inserire anche i flags , ad esempio overwrite=True
    options, flags = gs.parser()

# mi fa scegliere la mappa di input con i millimetri di pioggia
    mappa_pioggia = (options['rainfall_map'])

# mi fa scegliere le ore di pioggia
    ore = int(options['rainfall_period'])

# mi fa scegliere il file csv con le soglie di pioggia
    soglie=(options["rainfall_thresholds"])

# calcolo la pericolosità in base base alla soglia di pioggia (HR)
# come soglia di pioggia si intende altezza in mm riferita ad un determinato numero di ore

# trova il file .csv che ho prima definito come "soglie", lo legge e lo carica come DataFrame
# header=0 significa che la prima riga contiene le intestazioni di colonna
# index_col=0 significa che la prima colonna contiene l'indice, cioè le intestazioni di riga

    df = pd.read_csv(soglie, header=0, index_col=0)
#    print(f'{df}\n questo è il dataframe originale\n')

# traspongo il fil csv in modo da avere le soglie di pioggia in colonna
    df_girato=df.T
#    print(f'{df_girato}\n e questo è quello trasposto\n')

#mi definisce i valori di soglie s1, s2, s3 e s4 in base alla lista [ore] che ho definito sopra
    s1, s2, s3, s4 = df.loc[ore]

    formula = (
        f"HR = if({mappa_pioggia} < {s1}, 0, "
        f"if({mappa_pioggia} < {s2}, 0.75, "
        f"if({mappa_pioggia} < {s3}, 0.85, "
        f"if({mappa_pioggia} < {s4}, 0.9, 0.95))))"
    )

    gs.mapcalc(formula)

    WHR=0.3 
    WHB=0.7

# la dicitura "mappa_suscettivita" mi fa scegliere la mappa di input di suscettivita 
# questa riga fa riferimento alle linee "commentate" in alto
    mappa_suscettivita = (options['susceptibility_map'])

# trasformo le classi intere della mappa di suscettività nei valori riportati nella tabella (HB)
    gs.mapcalc('{r} = if({a}==0, 0, if({a}==1, 0.3, if({a}==2, 0.45, if({a}==3, 0.60, if({a}==4, 0.75, 0.95)))))'.format(r='HL', a=f'{mappa_suscettivita}'))

# calcolo la pericolosita H con la formula:
# se HR = 0 => H=0
# se HB = 0 => H=0
# se HR > 0 => H= HR*WHR + HB*WHB

# nel nome del file risultante metto il numero di ore, altrimenti se si lanciasse lo script per tante ore si rischia di confondersi o di sovrascrivere i risultati
    gs.mapcalc('{r} = if({a}==0 || {c}==0, 0, ({a}*{b})+({c}*{d}))'.format(r=f'hazard_{ore}h', a='HR', b=WHR, c='HL',d=WHB))

# rimuovo le mappe di lavoro
    gs.run_command('g.remove', type='raster', name='HL,HR', flags='f')

    colors = """0 white
                0.3 green
                0.5 yellow
                0.7 orange
                0.9 red
                1 purple
                """

    gs.write_command(
    "r.colors",
    map=f"hazard_{ore}h",
    rules="-",
    stdin=colors
)
     
   

if __name__ == '__main__':
    main()
