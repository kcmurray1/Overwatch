import { observer } from 'mobx-react-lite';
import { themeStore } from '../stores/ThemeStore';

export const ThemeToggle = observer(() => {
  return (
    <div>
   
      <input type="checkbox"
      aria-label="Toggle dark mode"
      onClick={() => {  themeStore.setTheme(themeStore.isDark ? 'light' : 'dark')}}
      />
      <label>{themeStore.isDark ?'Light':  'Dark'}</label>
    </div>
  );
});