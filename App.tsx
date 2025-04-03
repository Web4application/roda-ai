"use client";

import {
  LiveblocksProvider,
  RoomProvider,
} from "@liveblocks/react/suspense";
import { Editor } from "./Editor";

export default function App() {
  return (
    <LiveblocksProvider publicApiKey={"pk_prod_9KensGJpifraqw4oar3bVPl2T5Qh5W4NWUpdY0MwaUjA3RMH8gCLjfZyky9lyF77"}>
      <RoomProvider id="my-room">
        {/* ... */}
      </RoomProvider>
    </LiveblocksProvider>
  );
}
