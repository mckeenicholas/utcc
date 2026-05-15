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
		class="data-[state=unchecked]:shadow-mini-inset peer inline-flex h-[24px] min-h-[24px] w-[48px] shrink-0 cursor-pointer items-center rounded-full px-[2px] transition-colors focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 focus-visible:outline-hidden disabled:cursor-not-allowed disabled:opacity-50 data-[state=checked]:bg-blue-500 data-[state=unchecked]:bg-gray-200"
	>
		<Switch.Thumb
			class="data-[state=unchecked]:shadow-mini dark:shadow-popover pointer-events-none block size-[20px] shrink-0 rounded-full bg-white transition-transform data-[state=checked]:translate-x-6 data-[state=unchecked]:translate-x-0"
		/>
	</Switch.Root>
	<Label.Root for={id} class="cursor-pointer">{label}</Label.Root>
</div>
