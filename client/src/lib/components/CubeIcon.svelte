<script lang="ts">
	import { eventNames, type WCAEvent } from '$lib/types';
	import type { ClassValue } from 'svelte/elements';
	import '../icons.css';
	import { Tooltip } from 'bits-ui';

	const { event, class: className }: { event: WCAEvent; class?: ClassValue } = $props();
</script>

<Tooltip.Provider>
	<Tooltip.Root delayDuration={200}>
		<Tooltip.Trigger>
			<span class="icon cubing-icon event-{event} {className}"></span>
		</Tooltip.Trigger>
		<Tooltip.Content>
			<div class="rounded-md border bg-white px-2 ease-in-out">
				{eventNames[event]}
			</div>
		</Tooltip.Content>
	</Tooltip.Root>
</Tooltip.Provider>
