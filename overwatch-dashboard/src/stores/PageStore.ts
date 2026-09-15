import { makeAutoObservable } from "mobx";


export class PageStore {
    activePage: string = "home";

    constructor() {
        makeAutoObservable(this);
    }

    set page(pageName: string){
        this.activePage = pageName; 
    }
}

export const pageStore = new PageStore();