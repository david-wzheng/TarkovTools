/* eslint-disable @typescript-eslint/naming-convention */
import { DependencyContainer } from "tsyringe";
import { IPreAkiLoadMod } from "@spt-aki/models/external/IPreAkiLoadMod";
import { IPostDBLoadMod } from "@spt-aki/models/external/IPostDBLoadMod";
import { InstanceManager } from "./InstanceManager";
import { TraderTarkovTools } from "./Trader/Trader";

class Mod implements IPreAkiLoadMod, IPostDBLoadMod
{
    private Instance: InstanceManager = new InstanceManager()
    private traderTarkovTools: TraderTarkovTools = new TraderTarkovTools();

    private modName: string = "TarkovTools";
    debug = false;

    // Code added here will load BEFORE the server has started loading
    preAkiLoad(container: DependencyContainer): void 
    {
        // Initialize the instance manager DO NOTHING ELSE BEFORE THIS
        this.Instance.preAkiLoad(container, this.modName);
        this.Instance.debug = this.debug;
        // EVERYTHING AFTER HERE MUST USE THE INSTANCE
        this.traderTarkovTools.preAkiLoad(this.Instance)
    }

    postDBLoad(container: DependencyContainer): void
    {
        this.Instance.postDBLoad(container);
        this.traderTarkovTools.postDBLoad()
        this.Instance.questApi.loadQuestsRepeatableTemplateFromDisk()
    }
}

module.exports = { mod: new Mod() }