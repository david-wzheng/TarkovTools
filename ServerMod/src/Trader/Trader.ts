/* eslint-disable @typescript-eslint/naming-convention */
import { InstanceManager } from "../InstanceManager";
//import { CourierZones } from "./zones/CourierZones";

import { LogTextColor } from "@spt-aki/models/spt/logging/LogTextColor"


export class TraderTarkovTools
{
    mydb: any;
    private Instance: InstanceManager;
    private BaseJson;
    private Assort;
    private QuestAssort;

    public preAkiLoad(Instance: InstanceManager): void 
    {
        this.Instance = Instance;
        
        this.BaseJson = this.Instance.traderApi.loadTraderBaseJson("TarkovTools");
        this.Assort = this.Instance.traderApi.loadTraderAssortJson("TarkovTools");
        this.QuestAssort = this.Instance.traderApi.loadTraderQuestAssortJson("TarkovTools");

        this.Instance.traderApi.setupTrader("TarkovTools", this.BaseJson);
        
        
        this.Instance.logger.log(`[${this.Instance.modName}] Trader: TarkovTools Active`, LogTextColor.GREEN);
    }
    
    public postDBLoad(): void 
    {
        this.mydb = this.Instance.traderApi.loadTraderDbRecursive("TarkovTools");

        this.Instance.traderApi.addTraderToDb(this.mydb, "TarkovTools", 
            this.BaseJson, this.Assort, this.QuestAssort);

        //Load quests
        this.Instance.questApi.loadQuestsFromDirectory("TarkovTools");
        //this.Instance.questApi.importQuestZones(TarkovToolsZones, "TarkovTools");
    }
}