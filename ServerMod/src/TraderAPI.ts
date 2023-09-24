/* eslint-disable @typescript-eslint/naming-convention */
import path from "path";
import fs from "fs";

import { Traders } from "@spt-aki/models/enums/Traders";
import { ITraderAssort, ITraderBase } from "@spt-aki/models/eft/common/tables/ITrader";
import { ITraderConfig, UpdateTime } from "@spt-aki/models/spt/config/ITraderConfig";
import { ConfigTypes } from "@spt-aki/models/enums/ConfigTypes";
import { LogTextColor } from "@spt-aki/models/spt/logging/LogTextColor";
import { IRagfairConfig } from "@spt-aki/models/spt/config/IRagfairConfig";

import { InstanceManager } from "./InstanceManager";


export class TraderAPI
{
    private Instance: InstanceManager;

    private dbPath; 

    public preAkiLoad(Instance: InstanceManager): void
    {
        this.Instance = Instance;
        this.dbPath = path.join(this.Instance.dbPath, "\\Traders")
    }

    /**
     *  Trader to load database for 
     *  db/Traders/@param trader/{content}
     * @returns 
     */
    public loadTraderDbRecursive(trader: string): any
    {
        return this.Instance.importerUtil.loadRecursive(path.join(this.dbPath, `\\${trader}\\`));
    }

    /**
     * Load base.json for trader
     * db/Traders/@param trader/@param trader-base.json 
     * 
     * @returns 
     */
    public loadTraderBaseJson(trader: string): any
    {
        const file = fs.readFileSync(
            path.join(this.dbPath, `\\${trader}\\${trader}Base.json`), "utf8");
        const json = JSON.parse(file);
        return json;
    }

    /**
     * Load Assort.json for trader
     * db/Traders/@param trader/@param trader-Assort.json 
     * 
     * @returns 
     */
    public loadTraderAssortJson(trader: string): any
    {
        const file = fs.readFileSync(
            path.join(this.dbPath, `\\${trader}\\${trader}Assort.json`), "utf8");
        const json = JSON.parse(file);
        return json;
    }

    /**
     * Load QuestAssort.json for trader
     * db/Traders/@param trader/@param trader-Assort.json 
     * 
     * @returns 
     */
    public loadTraderQuestAssortJson(trader: string): any
    {
        const file = fs.readFileSync(
            path.join(this.dbPath, `\\${trader}\\${trader}QuestAssort.json`), "utf8");
        const json = JSON.parse(file);
        return json;
    }

    public setupTrader(trader: string, baseJson: any): void
    {
        const traderConfig: ITraderConfig = this.Instance.configServer.getConfig<ITraderConfig>(ConfigTypes.TRADER);

        const updateTime: UpdateTime = {
            traderId: baseJson._id,
            seconds: 3600
        };
        traderConfig.updateTime.push(updateTime);

        this.registerProfileImage(trader, baseJson);
        Traders[baseJson._id] = baseJson._id;
    }

    /**
     * 
     * @param mydb traders database       
     * @param trader traders name Ex. "GoblinKing"
     * @param baseJson traders base.json
     * @param assortJson traders assort.json
     * @param questAssortJson Traders quest assort
     */
    public addTraderToDb(mydb: any, trader: string, baseJson: any, assortJson: any,  questAssortJson: any): void
    {
        this.Instance.database.traders[baseJson._id] = {
            assort: this.Instance.jsonUtil.deserialize(this.Instance.jsonUtil.serialize(assortJson)) as ITraderAssort,
            base: JSON.parse(JSON.stringify({ ...baseJson, unlockedByDefault: true })) as ITraderBase,
            questassort: JSON.parse(JSON.stringify(questAssortJson))
        };

        const ragfairConfig: IRagfairConfig = this.Instance.configServer.getConfig(ConfigTypes.RAGFAIR);
        ragfairConfig.traders[baseJson._id] = true;

        
        let items = 0;
        for (const item in mydb.templates.items.items.templates) 
        {
            this.Instance.database.templates.items[item] = mydb.templates.items.items.templates[item];
            items++;
        }
        this.Instance.logger.log(`[${this.Instance.modName}] TraderAPI: ${trader} added ${items} to the database.`, LogTextColor.GREEN);


        
        const locales: Record<string, Record<string, string>> = this.Instance.database.locales.global;
        locales.en = {
            ...locales.en,
            ...mydb?.locales.en
        };
        this.Instance.logger.log(`[${this.Instance.modName}] TraderAPI: ${trader} added item locales.`, LogTextColor.GREEN);

        let handbooks = 0;
        for (const handbook of mydb.templates.handbook.Items) 
        {
            if (!this.Instance.database.templates.handbook.Items.find((i) => i.Id == handbook.Id)) 
                this.Instance.database.templates.handbook.Items.push(handbook);
            handbooks++;
        }
        this.Instance.logger.log(`[${this.Instance.modName}] TraderAPI: ${trader} added ${handbooks} items to handbook database.`, LogTextColor.GREEN);

        this.addTraderToLocales(trader, baseJson);

        this.Instance.logger.log(`[${this.Instance.modName}] TraderAPI: ${trader} successfully added to database.`, LogTextColor.GREEN);
    }

    /**
     * @param trader traders name "GoblinKing"
     * @param baseJson traders base.json
     */
    private addTraderToLocales(trader: string, baseJson: any): void 
    {
        const locales: Record<string, Record<string, string>> = this.Instance.database.locales.global;

        let count = 0;
        for (const locale in locales) 
        {
            locales[locale][`${baseJson._id} FullName`] = baseJson.name;
            locales[locale][`${baseJson._id} FirstName`] = baseJson.firstname;
            locales[locale][`${baseJson._id} Nickname`] = baseJson.nickname;
            locales[locale][`${baseJson._id} Location`] = baseJson.location;
            locales[locale][`${baseJson._id} Description`] = baseJson.description;
            count++;
        }

        this.Instance.logger.log(`[${this.Instance.modName}] TraderAPI: ${trader} loaded ${count} locales`, LogTextColor.GREEN);
    }

    private registerProfileImage(trader: string, baseJson: any): void 
    {
        const imageFilepath = `./${this.Instance.preAkiModLoader.getModPath(this.Instance.modName)}res`;
        this.Instance.imageRouter.addRoute(baseJson.avatar.replace(".png", ""), `${imageFilepath}/${trader}.png`);
    }
}