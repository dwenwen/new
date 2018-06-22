from bs4 import BeautifulSoup

xml = '''
<error>
    <ret>0</ret>
    <message></message>
    <skey>@crypt_86403b1b_8a5d080588bd9893201f65c17516ea54</skey>
    <wxsid>Dvb96Y09D3EBUyPo</wxsid>
    <wxuin>971127980</wxuin>
    <pass_ticket>1C%2FrwDplgJL6Fv%2F%2F1cXBKAEw9lPb7wOFDhOc%2FpF0RRKa%2FwC6ADUgxWq8X6HCoJzA</pass_ticket>
    <isgrayscale>1</isgrayscale>
</error>
'''
def xml_parser(xml):
    dic= {}
    soup = BeautifulSoup(xml,'html.parser')
    error = soup.find('error')
    ele_list = error.find_all(recursive=False)
    for i in ele_list:
        dic[i.name]=i.text
    return dic

