/* eslint-disable @typescript-eslint/naming-convention */
import * as path from "path";
import * as fs from "fs";
import { LogTextColor } from "@spt-aki/models/spt/logging/LogTextColor";
import { IQuest } from "@spt-aki/models/eft/common/tables/IQuest";
import { IRepeatableQuestDatabase } from "@spt-aki/models/eft/common/tables/IRepeatableQuests";
import { InstanceManager } from "./InstanceManager";

export interface QuestZone
{
    zoneId: string;
    zoneName: string;
    zoneType: string;
    zoneLocation: string;
    position: {
        x: string;
        y: string;
        z: string;
    }
    rotation: {
        x: string;
        y: string;
        z: string;
    }
    scale: {
        x: string;
        y: string;
        z: string;
    }
}

export class QuestAPI 
{
    private Instance: InstanceManager;

    private emptyDb: Record<string, IQuest> = {}

    /**
     * Call inside traders preAkiLoad method.
     * 
     * @param {ILogger} logger    Logger
     * @param {string}  mod       mod name
     * @return {void}             
     */
    public preAkiLoad(Instance: InstanceManager): void
    {
        this.Instance = Instance;
    }

    public postDBLoad(): void
    {
        this.Instance.database.globals["QuestZones"] = [];
        this.Instance.database.globals["FlareZones"] = [];
        this.Instance.database.globals["BotKillZones"] = [];
    }

    /**
     * Loads all quest files from disk.
     * \user\mods\WTTTeam-WelcomeToTarkov\db\quests\{trader}
     * \user\mods\WTTTeam-WelcomeToTarkov\db\quests\{trader}\locales
     * 
     * @param {string} trader     Trader to load quests for.
     * @return {any[]}            Returns an array of parsed json objects
     */
    public loadQuestsFromDirectory(trader: string): void
    {
        const jsonQuestFiles: any[] = [];
        const jsonLocaleFiles: any[] = [];
        const jsonImageFiles: any[] = [];
        const questFiles = fs.readdirSync(this.Instance.dbPath.concat(`\\Quests\\${trader}\\`));
        const questLocalesFiles = fs.readdirSync(this.Instance.dbPath.concat(`\\Quests\\${trader}\\locales`));
        const questImageFiles = fs.readdirSync(this.Instance.dbPath.concat(`\\Quests\\${trader}\\images`));

        if (this.Instance.debug)
        {
            console.log("---------------------------------------------------------");
            console.log(`Trader: ${trader} quest files:`);
            console.log(questFiles);
            console.log(`Trader: ${trader} locale files:`);
            console.log(questLocalesFiles);
            console.log(`Trader: ${trader} image files:`);
            console.log(questImageFiles);
            console.log("---------------------------------------------------------");
        }
        
        // Load quest data from disk
        for (const file of questFiles)
        {
            const filePath = path.join(this.Instance.dbPath.concat(`\\Quests\\${trader}`), file);
            const itemStats = fs.lstatSync(filePath);
            let fileContent: any;

            if (itemStats.isFile()) 
            {
                fileContent = fs.readFileSync(filePath, "utf-8");

                try 
                {
                    const jsonData = JSON.parse(fileContent);
                    jsonQuestFiles.push(jsonData);
                } 
                catch (error) 
                {
                    console.error(`Error parsing JSON from file ${filePath}: ${error}`);
                }
            }          
            
            if (this.Instance.debug)
            {
                console.log(`Trader: ${trader} quest file path:`)
                console.log(filePath);
            }      
        }
        
        // Load locale data from disk
        for (const locale of questLocalesFiles)
        {
            const filePath = path.join(this.Instance.dbPath.concat(`\\Quests\\${trader}\\locales`), locale);
            const itemStats = fs.lstatSync(filePath);
            let fileContent: any;

            if (itemStats.isFile()) 
            {
                fileContent = fs.readFileSync(filePath, "utf-8");
            }   

            if (this.Instance.debug)
            {
                console.log(`Trader: ${trader} quest locale file path:`)
                console.log(filePath);
            }

            try 
            {
                const jsonData = JSON.parse(fileContent);
                jsonLocaleFiles.push(jsonData);
            } 
            catch (error) 
            {
                console.error(`Error parsing JSON from file ${filePath}: ${error}`);
            }
        }
        
        // Load image paths from disk
        for (const image of questImageFiles)
        {
            const filePath = path.join(this.Instance.dbPath.concat(`\\Quests\\${trader}\\images`), image);
            const itemStats = fs.lstatSync(filePath);

            if (itemStats.isFile()) 
            {
                jsonImageFiles.push(filePath);
            }   

            if (this.Instance.debug)
            {
                console.log(`Trader: ${trader} quest image file path:`)
                console.log(filePath);
            }           
        }
        
        this.importQuestData(jsonQuestFiles, trader);
        this.importLocaleData(jsonLocaleFiles, trader);
        this.importImageData(jsonImageFiles, trader);
    }

    public loadQuestsRepeatableTemplateFromDisk(): void
    {
        const rQuestJsonString = fs.readFileSync(this.Instance.dbPath.concat("/Quests/repeatableQuests.json"), "utf-8");
        const jsonData: IRepeatableQuestDatabase = JSON.parse(rQuestJsonString) as IRepeatableQuestDatabase;
        this.Instance.database.templates.repeatableQuests = jsonData;
        if (this.Instance.debug)
        {
            console.log(this.Instance.database.templates.repeatableQuests);
        }
        this.Instance.logger.log(`[${this.Instance.modName}] QuestAPI: Loaded repeatableQuests.json`, LogTextColor.GREEN);
    }

    /**
     * Import quest zones.
     * 
     * @param {QuestZone} questZones     Trader to load quests zones for.
     * @return {void}                    Returns nothing
     */
    public importQuestZones(questZones: QuestZone[], trader: string): void 
    {
        let zones = 0;
        for (const zone of questZones)
        {
            if (this.Instance.debug)
            {
                console.log(zone);
            }
            this.Instance.database.globals["QuestZones"].push(zone);
            zones++;
        }
        this.Instance.logger.log(`[${this.Instance.modName}] QuestAPI:  ${trader} Loaded ${zones} quest zones.`, LogTextColor.GREEN);
    }

    /**
     * 
     * Wipe all quest data in the database
     * When I say all, I actually mean it...
     */
    public wipeQuestDb(): void 
    {
        this.Instance.database.templates.quests = this.emptyDb;
        this.Instance.logger.log(`[${this.Instance.modName}] QuestAPI: Wiped all base quest data.`, LogTextColor.GREEN);
    }

    private importQuestData(jsonQuestFiles: any[], trader: string): void
    {
        
        if (Object.keys(jsonQuestFiles).length < 1)
        {
            this.Instance.logger.log(`[${this.Instance.modName}] QuestAPI:  ${trader} No quest files.`, LogTextColor.RED); 
            return;
        }
        else
        {
            this.Instance.logger.log(`[${this.Instance.modName}] QuestAPI:  ${trader} Loading ${Object.keys(jsonQuestFiles).length} quest files.`, LogTextColor.GREEN);
        }
        
        // Import quest data to the database
        let questCount = 0;
        for (const file of jsonQuestFiles)
        {
            for (const quest in file)
            {
                this.Instance.database.templates.quests[quest] = file[quest];
                questCount++;
            }           
        }
        this.Instance.logger.log(`[${this.Instance.modName}] QuestAPI:  ${trader} Loaded ${questCount} tasks.`, LogTextColor.GREEN);      
    }

    private importLocaleData(jsonLocaleFiles: any[], trader: string): void
    {
        if (Object.keys(jsonLocaleFiles).length < 1)
        {
            this.Instance.logger.log(`[${this.Instance.modName}] QuestAPI:  ${trader} No quest locale files.`, LogTextColor.RED); 
            return;
        }
        else
        {
            this.Instance.logger.log(`[${this.Instance.modName}] QuestAPI:  ${trader} Loading ${Object.keys(jsonLocaleFiles).length} locale files.`, LogTextColor.GREEN);
        }

        // Import quest locales to the database
        let localeCount = 0;
        for (const file of jsonLocaleFiles)
        {
            for (const locale in file)
            {
                this.Instance.database.locales.global["en"][locale] = file[locale]
                localeCount++;
            }           
        }
        this.Instance.logger.log(`[${this.Instance.modName}] QuestAPI:  ${trader} Loaded ${localeCount} locales.`, LogTextColor.GREEN);
    }

    private importImageData(jsonImageFiles: any[], trader: string): void
    {
        let imageCount = 0;
        for (const imagePath of jsonImageFiles)
        {
            this.Instance.imageRouter.addRoute(`/files/quest/icon/${path.basename(imagePath, path.extname(imagePath))}`, imagePath);
            imageCount++;
        }
        this.Instance.logger.log(`[${this.Instance.modName}] QuestAPI:  ${trader} Loaded ${imageCount} images.`, LogTextColor.GREEN);
    }
}