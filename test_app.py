import unittest
from app import app
import werkzeug

# Patch temporário para adicionar o atributo '__version__' em
werkzeug
if not hasattr(werkzeug, '__version__'):
    werkzeug.__version__ = "mock-version"

class APITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Criação do cliente de teste
        cls.client = app.test_client()

    def test_home(self): #Verifica se a rota / responde com o status 200 e a mensagem correta.
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "API is running"})

    def test_login(self): #Confirma que a rota /login gera um token JWT.
        response = self.client.post('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json)

    def test_protected_no_token(self): #Testa o acesso à rota /protected sem o token JWT, esperando um status de não autorizado (401).
        response = self.client.get('/protected')
        self.assertEqual(response.status_code, 401)

    def test_items (self): #Verificando se a rota retorna a lista correta de itens
       response = self.client.get('/items')
       self.assertEqual(response.status_code, 200)
       self.assertEqual(response.json, {"items": ["item1", "item2", "item3"]})
    
    def test_login_metodo(self):  # Testa a rota /login com o método GET não permitido.
        response = self.client.get('/login')  # /login espera POST, não GET.
        self.assertEqual(response.status_code, 405)   
    
    def test_not_found(self):  # Testa uma rota inexistente para ver se retorna 404.
        response = self.client.get('/inexistente')
        self.assertEqual(response.status_code, 404)


    if __name__ == '__main__':
        unittest.main()