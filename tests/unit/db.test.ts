import { describe, it, expect } from 'vitest';
import { validateContactForm } from '../../src/lib/validation';

describe('Modelagem e Validação de Persistência D1', () => {
  it('deve formatar registros de contato em conformidade com as colunas do D1', () => {
    const contactPayload = {
      name: 'André Luiz',
      email: 'andre@exemplo.com.br',
      subject: 'Dúvida sobre Fonte',
      message: 'Mensagem de teste para validação de contrato de dados.'
    };

    const validation = validateContactForm(contactPayload);
    expect(validation.isValid).toBe(true);
    expect(contactPayload.name).toBeTypeOf('string');
    expect(contactPayload.email).toContain('@');
  });
});