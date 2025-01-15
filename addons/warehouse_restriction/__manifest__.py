{
    'name': 'Warehouse Restriction by User',
    'version': '1.0',
    'author': 'Santiago Gimenez',
    'category': 'Warehouse',
    'summary': 'Restricción de acceso a almacenes por usuario.',
    'description': 'Permite definir los almacenes permitidos a los usuarios de manera similar a la configuración multiempresa.',
    'depends': ['base', 'stock'],
    'data': [
        'security/warehouse_restriction_security.xml',
        'security/ir.model.access.csv',
        'views/res_users_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
