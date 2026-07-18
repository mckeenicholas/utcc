<script lang="ts">
interface Props {
	value: number;
	placeholder?: string;
	id: string;
	disabled?: boolean;
}

import { toInt } from "$lib/utils";

let { value = $bindable(0) }: Props = $props();
const { placeholder = "Enter time", id, disabled = false }: Props = $props();

const DNF_KEYS = new Set(["d", "D", "/", "#"]);
const DNS_KEYS = new Set(["s", "S", "*"]);

const ref: HTMLInputElement | null = $state(null);

const toCentiseconds = (input: string): number => {
	if (input === "") {
		return 0;
	}
	if (input === "DNF") {
		return -1;
	}
	if (input === "DNS") {
		return -2;
	}
	const num = toInt(input.replaceAll(/\D/gu, "")) || 0;
	return (
		Math.floor(num / 1_000_000) * 360_000 +
		Math.floor((num % 1_000_000) / 10_000) * 6000 +
		Math.floor((num % 10_000) / 100) * 100 +
		(num % 100)
	);
};

const toClockFormat = (centiseconds: number): string => {
	if (centiseconds === 0) {
		return "";
	}
	if (centiseconds === -1) {
		return "DNF";
	}
	if (centiseconds === -2) {
		return "DNS";
	}
	if (centiseconds === null || !Number.isFinite(centiseconds) || centiseconds < 0) {
		return "";
	}
	return new Date(centiseconds * 10)
		.toISOString()
		.slice(11, 22)
		.replaceAll(/^[0:]*(?!\.)/gu, "");
};

let displayValue = $derived(toClockFormat(value));

const reformatInput = (input: string): string => {
	const number = toInt(input.replaceAll(/\D/gu, "")) || 0;
	if (number === 0) {
		return "";
	}

	const str = `00000000${number.toString().slice(0, 8)}`;
	const match = str.match(/(\d\d)(\d\d)(\d\d)(\d\d)$/u);
	if (!match) {
		return "";
	}

	const [, hh, mm, ss, cc] = match;
	return `${hh}:${mm}:${ss}.${cc}`.replaceAll(/^[0:]*(?!\.)/gu, "");
};

const handleInput = (event: Event) => {
	const input = event.target as HTMLInputElement;
	const inputValue = input.value;
	const key = inputValue.slice(-1);

	if (inputValue.trim() === "") {
		displayValue = "";
	} else if (DNF_KEYS.has(key)) {
		displayValue = "DNF";
	} else if (DNS_KEYS.has(key)) {
		displayValue = "DNS";
	} else {
		displayValue = reformatInput(inputValue);
	}
};

const resetIfInvalid = (input: string) => {
	const time = toInt(input) ?? 60;
	if (time >= 60) {
		displayValue = "";
		value = 0;
	}
};

const handleUnfocus = () => {
	const input = displayValue.trim();

	if (input === "") {
		value = 0;
		return;
	}

	if (input === "DNF") {
		value = -1;
		return;
	}

	if (input === "DNS") {
		value = -2;
		return;
	}

	const timeParts = input.split(/[:.]/u).toReversed();

	if (timeParts.length >= 2) {
		resetIfInvalid(timeParts[1]);
	}

	if (timeParts.length >= 3) {
		resetIfInvalid(timeParts[2]);
	}

	value = toCentiseconds(displayValue);
};

const handleKeydown = (event: KeyboardEvent) => {
	if (event.key === "Enter" || event.key === "ArrowDown" || event.key === "+") {
		event.preventDefault();
		const inputs = document.querySelectorAll(".time-input");
		const currentIndex = [...inputs].indexOf(event.target as HTMLInputElement);
		const nextInput = inputs[currentIndex + 1] as HTMLInputElement;
		if (nextInput) {
			nextInput.focus();
		} else {
			const submitButton = document.querySelector(".submit-button") as HTMLButtonElement;
			if (submitButton) {
				submitButton.focus();
			}
		}
	} else if (event.key === "ArrowUp" || event.key === "-") {
		event.preventDefault();
		const inputs = document.querySelectorAll(".time-input");
		const currentIndex = [...inputs].indexOf(event.target as HTMLInputElement);
		const prevInput = inputs[currentIndex - 1] as HTMLInputElement;
		if (prevInput) {
			prevInput.focus();
		}
	}
};
</script>

<input
	{id}
	{disabled}
	bind:this={ref}
	class="time-input block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none disabled:cursor-not-allowed disabled:bg-gray-100 disabled:text-gray-500"
	type="text"
	inputmode="numeric"
	bind:value={displayValue}
	onblur={handleUnfocus}
	oninput={handleInput}
	onkeydown={handleKeydown}
	{placeholder}
/>
