import { observer } from 'mobx-react-lite';
import { themeStore } from '../stores/ThemeStore';

export const ThemeToggle = observer(() => {
  return (
    <div className='flex flex-row gap-2'>
      <input type="checkbox"
      aria-label="Toggle dark mode"
      onClick={() => {  themeStore.setTheme(themeStore.isDark ? 'light' : 'dark')}}
      />
      <label>{themeStore.isDark ?'Light':  'Dark'}</label>
    </div>
  );
});