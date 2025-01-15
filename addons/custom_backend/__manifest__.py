{
    'name': 'Custom CSS Injection',
    'version': '1.0',
    'category': 'Customization',
    'summary': 'Inject custom CSS in Odoo frontend or backend',
    'author': 'Tu Nombre',
    'website': 'https://tu-web.com',
    'depends': ['base', 'web'],  # Importante para agregar CSS al frontend y backend
    'data': [
        'views/custom_templates.xml',  # Archivo que contiene la referencia al CSS
    ],
    'assets': {},
    'installable': True,
    'application': False,
}
