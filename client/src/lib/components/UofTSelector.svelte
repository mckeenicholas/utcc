<script lang="ts">
import type { StudentStatus } from "$lib/types";
import MultiButton from "./MultiButton.svelte";

const { status = $bindable(), vertical = false }: { status: StudentStatus; vertical?: boolean } = $props();

const getIndex = (studentStatus: StudentStatus) => {
	switch (studentStatus) {
		case "uoft": {
			return 1;
		}
		case "non-uoft": {
			return 2;
		}
		default: {
			return 0;
		}
	}
};

const getStatus = (index: number) => {
	switch (index) {
		case 1: {
			return "uoft";
		}
		case 2: {
			return "non-uoft";
		}
		default: {
			return "all";
		}
	}
};
</script>

<MultiButton
	bind:selectedIndex={
		() => getIndex(status),
		(index) => {
			status = getStatus(index);
		}
	}
	labels={["All Students", "UofT Only", "Non-Uoft Only"]}
	{vertical}
></MultiButton>
