import ru from '../locales/ru/common.json'
import config from '../next.config.js';

const defaultLocale = config.i18n.defaultLocale;

const translations = {
    "ru": ru,
}

export function useTranslation(locale: string) {
  return translations[locale] || translations[defaultLocale];
}