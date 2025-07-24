/*
 * Auto-generated TypeScript module for DeviceRenderOptions
 */

export class DeviceRenderOptions {
    sdkInterface?: DeviceRenderOptions.SdkInterfaceEnum;
    sdkUiType?: Array<DeviceRenderOptions.SdkUiTypeEnum>;

    constructor(data?: Partial<DeviceRenderOptions>) {
        if (data) {
            this.sdkInterface = data.sdkInterface;
            this.sdkUiType = data.sdkUiType;
        }
    }
}

export namespace DeviceRenderOptions {
    export enum SdkInterfaceEnum {
        Native = 'native',
        Html = 'html',
        Both = 'both'
    }
    export enum SdkUiTypeEnum {
        MultiSelect = 'multiSelect',
        OtherHtml = 'otherHtml',
        OutOfBand = 'outOfBand',
        SingleSelect = 'singleSelect',
        Text = 'text'
    }
}
