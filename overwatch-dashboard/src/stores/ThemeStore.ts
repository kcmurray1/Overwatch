import { makeAutoObservable, runInAction } from 'mobx';

export type Theme = 'light' | 'dark' | 'system';

class ThemeStore {
  theme: Theme = (localStorage.getItem('theme') as Theme) || 'system';
  isDark: boolean = false;

  constructor() {
    makeAutoObservable(this);
    this.init();
  }

  private init() {
    this.applyTheme();

    // Listen for system preference changes
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    mediaQuery.addEventListener('change', () => {
      if (this.theme === 'system') {
        this.applyTheme();
      }
    });
  }

  setTheme(newTheme: Theme) {
    this.theme = newTheme;

    if (newTheme === 'system') {
      localStorage.removeItem('theme');
    } else {
      localStorage.setItem('theme', newTheme);
    }

    this.applyTheme();
  }

  private applyTheme() {
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const shouldBeDark =
      this.theme === 'dark' || (this.theme === 'system' && systemPrefersDark);

    runInAction(() => {
      this.isDark = shouldBeDark;
    });

    if (shouldBeDark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }
}

export const themeStore = new ThemeStore();