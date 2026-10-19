import { observer } from "mobx-react-lite/src/observer.js";

export interface BaseModalProps {
    isOpen: boolean
    onClose: ()=>void
    children?: React.ReactNode
    maxWidth?: string
}

export const BaseModal = observer(({isOpen, onClose, children, maxWidth = "max-w-lg"}: BaseModalProps) => {

    if (!isOpen) return;
    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-surface-card-light/60 backdrop-blur-sm animate-fade-in">
        
        <div 
        className="fixed inset-0" 
        onClick={onClose} 
        aria-hidden="true" 
        />
       <div 
        className={`relative z-10 w-full ${maxWidth} overflow-hidden rounded-xl
             bg-white p-6 shadow-2xl transition-all dark:bg-surface-card-dark text-zinc-900 dark:text-zinc-100`}
        role="dialog"
        aria-modal="true"
      >{children}</div>
      </div>
    )
});