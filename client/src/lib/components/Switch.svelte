<script lang="ts">
import type { ClassValue } from "svelte/elements";
import { Label, Switch, useId } from "bits-ui";

let {
	id = useId(),
	label,
	checked = $bindable(false),
	class: classProps,
}: { id?: string; label: string; checked?: boolean; class?: ClassValue } = $props();
</script>

<div class="me-2 flex items-center gap-x-2 {classProps}">
	<Switch.Root
		bind:checked
		{id}
		class="peer inline-flex h-[22px] min-h-[22px] w-[44px] shrink-0 cursor-pointer items-center rounded-full px-[2px] transition-colors focus-visible:ring-2 focus-visible:ring-uoft-blue focus-visible:ring-offset-1 focus-visible:outline-hidden disabled:cursor-not-allowed disabled:opacity-50 data-[state=checked]:bg-uoft-blue data-[state=unchecked]:bg-gray-200"
	>
		<Switch.Thumb
			class="pointer-events-none block size-[18px] shrink-0 rounded-full bg-white transition-transform data-[state=checked]:translate-x-[22px] data-[state=unchecked]:translate-x-0"
		/>
	</Switch.Root>
	<Label.Root for={id} class="cursor-pointer text-xs font-medium text-gray-700 select-none">{label}</Label.Root>
</div>
