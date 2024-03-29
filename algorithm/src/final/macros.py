HEBREW_TO_ENGLISH_FACILITIES = {
    'לא משנה מיקום': 'Any_place',
    'ראשי': 'Raashi',
    'מעצ': 'Maatz',
    'כורש': 'Koresh',
    'עררים': 'Ararim',
    'אזרחית': 'Ezrachit',
    'רשות התאגידים': 'Rashut_hataagidim',
    'אפכ ארצי': 'Apak_ertsi',
    'פטנטים': 'Patentim',
    'מלך דוד': 'Melech_david',
    'שרעי': 'Sharai',
    'רשם מקרקעין': 'Rasham_mekarkein',
    'טאבו מפקח': 'Tabu_mifkach',
    'סנגוריה': 'Sanagoria',
    'סיוע משפטי': 'Siyua_mishpati',
    'יחידת הסדר': 'Yechidat_haseder',
    'ועדת ערער': 'Vaadat_arar',
    'מחש': 'Machash',
    'מערכות מידע': 'Maarachot_meida',
    'רשם ירושות': 'Rasham_yerushot',
    'יחידות מקצועיות': 'Yechidot_miktsoiot',
}
# Dictionary to map Hebrew facility names to English facility names

# Dictionary to map Hebrew shifts names to English shifts names
HEBREW_TO_ENGLISH_SHIFTS = {
    'לא משנה שעה': 'Any_hour',
    '7:00-15:00': 'Morning',
    '15:00-23:00': 'Afternoon',
    '23:00-7:00': 'Night',
    '7:00-19:00': 'Double Morning',
    '19:00-7:00': 'Double Night'
}

# Dictionary to map Hebrew day names to English day names
HEBREW_TO_ENGLISH_DAYS = {
    'ראשון': 'Sunday',
    'שני': 'Monday',
    'שלישי': 'Tuesday',
    'רביעי': 'Wednesday',
    'חמישי': 'Thursday',
    'שישי': 'Friday',
    'שבת': 'Saturday'
}

facilities_names = [
    'Raashi', 'Maatz', 'Koresh', 'Yehidat_hataagidim', 'Apak_ertsi', 'Patentim',
    'Melech_david', 'Sharai', 'Rasham_mekarkein', 'Tabu_mifkach', 'Sanagoria',
    'Siyua_mishpati', 'Yechidat_haseder', 'Ezrachit', 'Ararim', 'Vaadat_arar',
    'Machash', 'Maarachot_meida', 'Rasham_yerushot', 'Yechidot_miktsoiot',
]

file_name = '../../work.csv'

raashi_morning = 7
raashi_afternoon = 5
raashi_night = 4
raashi_small_shift = 3

Maatz_morning = 3
Maatz_small_shift = 2

full_week = 7
short_week = 5
