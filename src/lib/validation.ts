export interface ContactFormData {
  name: string;
  email: string;
  subject: string;
  message: string;
}

export interface ValidationResult {
  isValid: boolean;
  errors: Record<string, string>;
}

export function validateContactForm(data: Partial<ContactFormData>): ValidationResult {
  const errors: Record<string, string> = {};

  if (!data.name || data.name.trim().length < 2) {
    errors.name = 'O nome deve conter pelo menos 2 caracteres.';
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!data.email || !emailRegex.test(data.email.trim())) {
    errors.email = 'Informe um endereço de e-mail válido.';
  }

  if (!data.subject || data.subject.trim().length < 3) {
    errors.subject = 'O assunto deve ter no mínimo 3 caracteres.';
  }

  if (!data.message || data.message.trim().length < 10) {
    errors.message = 'A mensagem deve conter pelo menos 10 caracteres.';
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
}