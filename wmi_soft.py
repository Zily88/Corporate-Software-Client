import wmi

w = wmi.WMI()

with open('wmi_product.txt', 'w', encoding='utf-8') as file:
    file.write('{0:64} {1:32}\n\n'.format('Name', 'Version'))
    for product in w.Win32_Product():
        file.write('{0:64} {1:32}\n'.format(product.Caption, product.Version))
