package net.cpbackend.stabilimento;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.springframework.http.HttpStatus.BAD_REQUEST;
import static org.springframework.http.HttpStatus.NOT_FOUND;

import org.junit.jupiter.api.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.test.context.junit4.SpringRunner;

import net.cpbackend.model.Stabilimento;

@RunWith(SpringRunner.class)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class InvalidStabilimentoTest {

	@Autowired
	private TestRestTemplate restTemplate;
	
	@Test
	void createStabilimentoInvalidData() {
		ResponseEntity<Stabilimento> response = restTemplate.postForEntity("/officina/stabilimenti", new Stabilimento(null),
				Stabilimento.class);

		assertEquals(BAD_REQUEST.value(), response.getStatusCode().value());
	}
	
	@Test
	void findByIdNotFound() {
		ResponseEntity<Stabilimento> response = restTemplate.getForEntity("/officina/stabilimenti/{id}",
				Stabilimento.class, Long.MAX_VALUE);

		assertEquals(NOT_FOUND.value(), response.getStatusCode().value());
	}
	
	@Test
	void updateStabilimentoInvalidData() {
		ResponseEntity<Stabilimento> response = restTemplate.exchange("/officina/stabilimenti/{id}", HttpMethod.PUT,
				new HttpEntity<>(null), Stabilimento.class, 1L);

		assertEquals(BAD_REQUEST.value(), response.getStatusCode().value());
	}
	
	@Test
	void updateStabilimentoNotFound() {
		Stabilimento stabilimento = new Stabilimento("test");
		stabilimento.setId(Long.MAX_VALUE);

		ResponseEntity<Stabilimento> response = restTemplate.exchange("/officina/stabilimenti/{id}", HttpMethod.PUT,
				new HttpEntity<>(stabilimento), Stabilimento.class, Long.MAX_VALUE);

		assertEquals(NOT_FOUND.value(), response.getStatusCode().value());
	}
	
	@Test
	void deleteStabilimentoNotFound() {
		ResponseEntity<Stabilimento> response = restTemplate.exchange("/officina/stabilimenti/{id}", HttpMethod.DELETE,
				null, Stabilimento.class, Long.MAX_VALUE);

		assertEquals(NOT_FOUND.value(), response.getStatusCode().value());
	}

}
