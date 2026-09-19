import { observer } from "mobx-react-lite/src/observer.js";

export interface BaseModalProps {
    isOpen: boolean
    onClose: ()=>void
    children?: React.ReactNode
}

export const BaseModal = observer(({isOpen, onClose, children}: BaseModalProps) => {

    if (!isOpen) return;
    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fade-in">
        
        <div 
        className="fixed inset-0" 
        onClick={onClose} 
        aria-hidden="true" 
        />
       <div 
        className="relative z-10 w-full max-w-lg overflow-hidden rounded-xl bg-white p-6 shadow-2xl transition-all dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 text-zinc-900 dark:text-zinc-100"
        role="dialog"
        aria-modal="true"
      >{children}</div>
      </div>
    )
});