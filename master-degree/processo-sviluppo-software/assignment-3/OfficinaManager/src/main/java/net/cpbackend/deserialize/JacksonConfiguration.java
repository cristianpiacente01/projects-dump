package net.cpbackend.deserialize;

import com.fasterxml.jackson.databind.ObjectMapper;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import com.fasterxml.jackson.databind.module.SimpleModule;

import net.cpbackend.model.Attrezzo;

@Configuration
public class JacksonConfiguration {

	@Bean
	public ObjectMapper objectMapper() {
		ObjectMapper mapper = new ObjectMapper();

		// create a module with the custom deserializer and register it on the object mapper
		
		SimpleModule customModule = new SimpleModule();
		customModule.addDeserializer(Attrezzo.class, new AttrezzoDeserializer());
		mapper.registerModule(customModule);

		return mapper;
	}
}