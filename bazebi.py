import sqlite3

# მონაცემთა ბაზის შექმნა
conn = sqlite3.connect("cars.sqlite")
cursor = conn.cursor()

# ცხრილის შექმნა
cursor.execute('''
    CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        country TEXT,
        cylinders TEXT,
        price_range TEXT,
        model TEXT
    )
''')

# მონაცემები (tuple სვეტებით: country, cylinders, price_range): model
cars_data = {
    ('იტალია', '6', '50k-100K$'): 'Alfa Romeo Giulia Quadrifoglio',
    ('იტალია', '6', '100K-500k$'): 'Lancia Stratos',
    ('იტალია', '6', '500K-2M$'): 'Ferrari Dino 246 GT',
    ('იტალია', '8', '50k-100K$'): 'Maserati GranSport',
    ('იტალია', '8', '100K-500k$'): 'Ferrari F430',
    ('იტალია', '8', '500K-2M$'): 'Ferrari 458 Speciale',
    ('იტალია', '10', '50k-100K$'): 'Lamborghini Gallardo',
    ('იტალია', '10', '100K-500k$'): 'Lamborghini Huracán',
    ('იტალია', '10', '500K-2M$'): 'Lamborghini Huracán STO',

    ('გერმანია', '6', '50k-100K$'): 'BMW M2 Competition',
    ('გერმანია', '6', '100K-500k$'): 'Porsche 911 Carrera S',
    ('გერმანია', '6', '500K-2M$'): 'Porsche 959',
    ('გერმანია', '8', '50k-100K$'): 'Mercedes-AMG C63',
    ('გერმანია', '8', '100K-500k$'): 'Audi R8 V8',
    ('გერმანია', '8', '500K-2M$'): 'Mercedes-AMG GT Black Series',
    ('გერმანია', '10', '50k-100K$'): 'BMW M5 E60',
    ('გერმანია', '10', '100K-500k$'): 'Audi R8 V10',
    ('გერმანია', '10', '500K-2M$'): 'Porsche Carrera GT',

    ('იაპონია', '6', '50k-100K$'): 'Nissan 370Z NISMO',
    ('იაპონია', '6', '100K-500k$'): 'Toyota Supra TRD 3000GT',
    ('იაპონია', '6', '500K-2M$'): 'Nissan GT-R R34 Z-Tune',
    ('იაპონია', '8', '50k-100K$'): 'Lexus IS F',
    ('იაპონია', '8', '100K-500k$'): 'Lexus LFA',
    ('იაპონია', '8', '500K-2M$'): 'Lexus LFA Nürburgring Edition',
    ('იაპონია', '10', '50k-100K$'): 'Honda/Acura NSX Gen 1',
    ('იაპონია', '10', '100K-500k$'): 'Honda/Acura NSX Gen 2 (2016+)',
    ('იაპონია', '10', '500K-2M$'): 'Honda NSX GT3'
}

# მონაცემების ჩასმა
for (country, cylinders, price_range), model in cars_data.items():
    cursor.execute('''
        INSERT INTO cars (country, cylinders, price_range, model)
        VALUES (?, ?, ?, ?)
    ''', (country, cylinders, price_range, model))

# შენახვა და დახურვა
conn.commit()
conn.close()

print("მონაცემთა ბაზა წარმატებით შეიქმნა და შევსდა.")
