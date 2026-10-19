import { describe, it, expect } from 'vitest';
import { validateContactForm } from '../../src/lib/validation';

describe('Validação do Formulário de Contato', () => {
  it('deve aprovar dados válidos', () => {
    const validData = {
      name: 'João Silva',
      email: 'joao@exemplo.com',
      subject: 'Sugestão de Fonte',
      message: 'Gostaria de sugerir a inclusão de um novo veículo de notícias.'
    };

    const result = validateContactForm(validData);
    expect(result.isValid).toBe(true);
    expect(Object.keys(result.errors)).toHaveLength(0);
  });

  it('deve reprovar campos em branco ou formatos inválidos', () => {
    const invalidData = {
      name: 'A',
      email: 'email-invalido',
      subject: 'Oi',
      message: 'Curto'
    };

    const result = validateContactForm(invalidData);
    expect(result.isValid).toBe(false);
    expect(result.errors.name).toBeDefined();
    expect(result.errors.email).toBeDefined();
    expect(result.errors.subject).toBeDefined();
    expect(result.errors.message).toBeDefined();
  });
});