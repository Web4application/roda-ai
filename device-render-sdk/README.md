# Device Render SDK

A TypeScript class for describing rendering options in a secure challenge SDK.

## Usage

```ts
import { DeviceRenderOptions } from "device-render-sdk";

const options = new DeviceRenderOptions({
  sdkInterface: DeviceRenderOptions.SdkInterfaceEnum.Native,
  sdkUiType: [DeviceRenderOptions.SdkUiTypeEnum.Text, DeviceRenderOptions.SdkUiTypeEnum.SingleSelect]
});
